from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class CategorizedLists(Generic[T]):
    todo: list[T]
    doing: list[T]
    done: list[T]
