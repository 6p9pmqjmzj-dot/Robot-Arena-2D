"""Small, reusable AABB collision helpers."""
from __future__ import annotations
from typing import Protocol


class HasBounds(Protocol):
    def get_bounds(self) -> tuple[float, float, float, float]: ...


def check_collision(first: HasBounds, second: HasBounds) -> bool:
    """Return true when two axis-aligned rectangles overlap."""
    ax1, ay1, ax2, ay2 = first.get_bounds()
    bx1, by1, bx2, by2 = second.get_bounds()
    return ax1 < bx2 and ax2 > bx1 and ay1 < by2 and ay2 > by1


def check_bounds(x: float, y: float, half_w: float, half_h: float,
                 left: float, right: float, bottom: float, top: float) -> bool:
    """Return whether a rectangle remains inside an arena."""
    return left + half_w <= x <= right - half_w and bottom + half_h <= y <= top - half_h
