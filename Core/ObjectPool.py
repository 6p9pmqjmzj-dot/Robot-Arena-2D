"""Reusable object pool."""
from __future__ import annotations
from typing import Callable, Generic, TypeVar
T = TypeVar("T")


class ObjectPool(Generic[T]):
    """Keeps turtle objects alive and reuses them instead of reallocating."""
    def __init__(self, factory: Callable[[], T], initial: int = 0) -> None:
        self.factory, self.available, self.in_use = factory, [], []
        for _ in range(initial): self.available.append(factory())

    def get(self) -> T:
        item = self.available.pop() if self.available else self.factory()
        self.in_use.append(item); return item

    def release(self, item: T) -> None:
        if item in self.in_use:
            getattr(item, "reset")(); self.in_use.remove(item); self.available.append(item)

    def clear(self) -> None:
        for item in self.in_use[:]: self.release(item)
