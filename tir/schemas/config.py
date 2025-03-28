from pathlib import Path
from typing import List, Optional, Any

from pydantic import BaseModel, ConfigDict, PositiveInt

from tir.utils import to_kebab


class ConfigMeta(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_kebab,
        populate_by_name=True
    )

    description: str
    title: str
    copyright: Optional[str]


class ConfigSite(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_kebab,
        populate_by_name=True
    )

    title: str
    tagline: Optional[str]


class NavigationItem(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_kebab,
        populate_by_name=True,
    )

    link: str
    title: str


class HomeContentElement(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_kebab,
        populate_by_name=True,
    )

    name: str
    url: str


class HomeContent(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_kebab,
        populate_by_name=True,
    )

    section: str
    elements: List[HomeContentElement]


class Visuals(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_kebab,
        populate_by_name=True
    )

    theme: str = 'default'


class Config(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_kebab,
        populate_by_name=True,
    )

    build_dir: str
    meta: ConfigMeta
    navigation: List[NavigationItem]
    recent_post_counter: PositiveInt = 5
    home_content: List[HomeContent]
    visuals: Visuals
    file_extension: str = 'html'
    lang: str = 'en_US'
    working_dir: Any = Path.cwd()

    def model_post_init(self, __context):
        self.file_extension = "" if self.file_extension is None else f'.{self.file_extension}'
