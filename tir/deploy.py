import hashlib
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar, List, Set, Any

import marshmallow_dataclass
import paramiko
import yaml
from paramiko import SFTPClient, SSHClient

from tir.cache import Cache
from tir.config import get_config
from tir.files import acquire_files
from tir.posts import Post
from tir.printers import cprint
from tir.schemas.config import Deployment
from tir.schemas.deploy import LockFile, LockFileItem, StaticFile


@dataclass
class Deploy:
    LOCK_FILE_PATH: ClassVar[str] = 'tir.lock'
    posts: Set[Post] = field(default_factory=acquire_files)
    static_files: List[StaticFile] = field(default_factory=list)
    config: Deployment = get_config().deployment
    ssh_client: SSHClient = None
    sftp_client: SFTPClient = None
    local_lock_file: LockFile = None
    remote_lock_file: LockFile = None

    def __post_init__(self):
        self._check_deployment_config()

    def _check_deployment_config(self):
        if not self.config:
            sys.exit(
                'Deployment not configured. Please check settings before proceeding to deployment.')

    def _hash_built_files(self) -> List[LockFileItem]:
        locked_items = []

        path = Path.cwd().joinpath(get_config().build_dir)

        for p in filter(lambda x: x.is_file(), path.rglob("*")):
            with p.open(mode="rb") as f:
                static_file = StaticFile()
                static_file.path = p.relative_to(get_config().working_dir.joinpath(
                    get_config().build_dir)).as_posix()
                lockfile_item = LockFileItem(
                    p.relative_to(get_config().working_dir.joinpath(get_config().build_dir)).as_posix(),
                    hashlib.blake2s(f.read()).hexdigest())
            self.static_files.append(static_file)
            locked_items.append(lockfile_item)
        return locked_items

    def _lock(self):
        lock_file: LockFile = LockFile()
        lock_file.content = self._hash_built_files()

        self.local_lock_file = lock_file

        lock_file_writable = marshmallow_dataclass.class_schema(
            LockFile)().dump(lock_file)

        with Path.cwd().joinpath(self.LOCK_FILE_PATH).open(mode='w+') as f:
            yaml.dump(lock_file_writable, f)

    def connect(self):
        k = paramiko.RSAKey.from_private_key_file(self.config.key_file)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.config.host, port=self.config.port,
                       username=self.config.username, pkey=k)
        self.ssh_client = client
        self.sftp_client = self.ssh_client.open_sftp()

    def _get_remote_lock(self) -> Any | None:
        c = Cache()
        dc = c.create_deployment_cache(self.config)
        try:
            _cached_remote_lock_file = dc.joinpath(self.LOCK_FILE_PATH)
            self.sftp_client.get(Path(self.config.path).joinpath(
                self.LOCK_FILE_PATH).as_posix(), _cached_remote_lock_file.as_posix())
            with _cached_remote_lock_file.open(mode='r') as f:
                lock_file_dict = yaml.safe_load(f.read())
                lock_file_remote = marshmallow_dataclass.class_schema(
                    LockFile)().load(lock_file_dict)
            self.remote_lock_file = lock_file_remote
            return lock_file_remote
        except FileNotFoundError:
            print(
                'Remote lock file does not exist. Is this the first time you are deploying static files?')

        return None

    def _clean_folders(self, path: str):
        files = self.sftp_client.listdir_attr(path)
        for file in files:
            path_remove = Path(path).joinpath(file.filename).as_posix()
            try:
                self.sftp_client.remove(path_remove)
            except IOError:
                self._clean_folders(path_remove)
        if self.config.path is not path:
            self.sftp_client.rmdir(path)

    def _upload_file(self, f: LockFileItem | StaticFile):

        if isinstance(f, LockFileItem):
            lf = StaticFile()
            lf.path = f.path
            f = lf

        def _create_parent_directory(p: Path):
            path_to_create = '/'.join(p.parts[:-1])[1:]
            try:
                self.sftp_client.mkdir(path_to_create)
            except FileNotFoundError:
                print(f'Could not create {path_to_create}')
                _create_parent_directory(Path(path_to_create))

        local_file_path = Path.cwd().joinpath(get_config().build_dir).joinpath(f.path)
        remote_file_path = Path(self.config.path).joinpath(f.path)

        try:
            self.sftp_client.put(local_file_path.as_posix(), remote_file_path.as_posix())
            print(f'Uploaded {remote_file_path}')
        except FileNotFoundError:
            _create_parent_directory(remote_file_path)
            self._upload_file(f)

    def _compare_lock_files(self) -> bool:
        to_update = []
        to_add = []
        surplus = self.remote_lock_file.content
        if self.remote_lock_file and self.local_lock_file:
            if self.remote_lock_file.content == self.local_lock_file.content:
                return True
            print(self.remote_lock_file)
            for local_item in self.local_lock_file.content:
                matched_item = None
                for remote_item in self.remote_lock_file.content:
                    if local_item.path == remote_item.path:
                        matched_item = remote_item
                        surplus.remove(matched_item)

                if matched_item:
                    if not local_item.signature == matched_item.signature:
                        print(
                            f'{local_item.path} exists but local signature ({local_item.signature}) is different from '
                            f'remote signature ({matched_item.signature}), will be updated '
                            f'update list')
                        to_update.append(local_item)
                    pass
                else:
                    print(f'{local_item.path} was not matched')
                    to_add.append(local_item)
        else:
            print('Either local and/or remote file(s) is/are empty')
            print(self.local_lock_file)

        if surplus:
            for item in surplus:
                self.sftp_client.remove(Path(self.config.path).joinpath(item.path).as_posix())

        if to_add:
            for item in to_add:
                self._upload_file(item)
        if to_update:
            for item in to_update:
                self._upload_file(item)

        cprint('GREEN', f'{len(to_add)} file(s) deleted.')
        cprint('YELLOW', f'{len(to_update)} file(s) updated.')
        cprint('RED', f'{len(surplus)} file(s) deleted.')

    def deploy(self):
        self._lock()
        self.connect()

        if self._get_remote_lock() is None:
            self._clean_folders(self.config.path)
            for sf in self.static_files:
                self._upload_file(sf)
        if self.remote_lock_file:
            self._compare_lock_files()
        self.sftp_client.put(get_config().working_dir.joinpath(self.LOCK_FILE_PATH).as_posix(),
                             Path(self.config.path).joinpath(self.LOCK_FILE_PATH).as_posix())
        self.ssh_client.close()
