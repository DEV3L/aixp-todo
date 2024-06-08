from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class CategorizedLists(Generic[T]):
    planning: list[T] = field(default_factory=list)
    todo: list[T] = field(default_factory=list)
    doing: list[T] = field(default_factory=list)
    done: list[T] = field(default_factory=list)
    users: list[T] = field(default_factory=list)
    team: list[T] = field(default_factory=list)

    def to_dict(self) -> dict:
        def serialize(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            return obj

        return asdict(self, dict_factory=lambda x: {k: serialize(v) for k, v in x})
