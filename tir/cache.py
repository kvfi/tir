from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar

from tir.schemas.config import Deployment


@dataclass
class Cache:
    DEFAULT_PATH: ClassVar[str] = '.tir_cache'
    path: Path = field(init=False)

    def __post_init__(self):
        self.path = Path.cwd() / self.DEFAULT_PATH
        if not self.path.exists():
            self.path.mkdir()

    def create_deployment_cache(self, config: Deployment) -> Path:
        deployment_cache_path = self.path.joinpath('deployments')
        deployment_cache_path.mkdir(exist_ok=True)
        deployment_cache_folders = [
            x for x in deployment_cache_path.iterdir() if not x.is_file()]

        deployement_id: int = max(
            [int(d.name) for d in deployment_cache_folders]) if deployment_cache_folders else -1
        deployement_id = deployement_id + 1

        deployment_cache_folder_path = deployment_cache_path.joinpath(
            str(deployement_id))
        deployment_cache_folder_path.mkdir()

        return deployment_cache_folder_path
