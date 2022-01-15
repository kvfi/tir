import time
from dataclasses import field
from pathlib import Path
from typing import Any, List, Set

from marshmallow import Schema
from marshmallow_dataclass import dataclass


@dataclass
class LockFileItem(Schema):
    path: str
    signature: str


@dataclass
class LockFile(Schema):
    last_deployment: float = field(default=time.time())
    content: List[LockFileItem] = field(default_factory=list)


@dataclass
class StaticFile(Schema):
    content: bytes = None
    path: Any = field(default_factory=Path.cwd)


'''@dataclass
class DeltaLock:
    to_delete: Set[Path]
'''