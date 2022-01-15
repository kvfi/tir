from dataclasses import field
from datetime import datetime
from pathlib import Path, PosixPath, WindowsPath
from typing import ClassVar, List, Optional, Type, Union, Any

from marshmallow import Schema, fields
from marshmallow_dataclass import dataclass


@dataclass
class Deployment(Schema):
    class Meta:
        ordered: True

    host: str
    port: int
    path: str
    username: str
    password: Optional[str]
    key_file: Optional[str] = field(metadata=dict(data_key='key-file'))
    Schema: ClassVar[Type[Schema]] = Schema


@dataclass
class ConfigMeta(Schema):
    class Meta:
        ordered: True

    description: str
    title: str
    copyright: Optional[str]
    Schema: ClassVar[Type[Schema]] = Schema


@dataclass
class NavigationItem(Schema):
    class Meta:
        ordered: True

    link: str
    title: str
    Schema: ClassVar[Type[Schema]] = Schema


@dataclass
class Visuals(Schema):
    class Meta:
        ordered: True

    theme: str = field(default="default")
    Schema: ClassVar[Type[Schema]] = Schema


@dataclass
class Config(Schema):
    class Meta:
        ordered: True

    build_dir: str
    deployment: Optional[Deployment]
    meta: ConfigMeta = field(default_factory=dict)
    navigation: List[NavigationItem] = field(default_factory=list)
    show_home_posts: bool = field(
        metadata=dict(data_key='show-home-posts'), default=False)
    visuals: Visuals = field(default_factory=Visuals)
    file_extension: str = field(
        default='html', metadata=(dict(missing=False, allow_none=True)))
    lang: str = field(default='en_US')
    working_dir: Any = field(default=Path.cwd())
    Schema: ClassVar[Type[Schema]] = Schema

    def __post_init__(self):
        self.file_extension = "" if self.file_extension is None else f'.{self.file_extension}'
