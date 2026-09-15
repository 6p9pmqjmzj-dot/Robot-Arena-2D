"""Projectile base class."""
from __future__ import annotations
import math
import turtle
from Core.Entity import Entity


class Projectile(Entity):
    """A reusable moving energy bolt."""
    def __init__(self, screen: turtle.Screen, color: str) -> None:
        super().__init__(screen, "circle", color, 10, 10)
        self.damage = 0.0; self.speed = 0.0; self.direction = (0.0, 1.0); self.owner = ""

    def activate(self, x: float, y: float, direction: tuple[float, float], damage: float) -> None:
        length = math.hypot(*direction) or 1; self.x, self.y = x, y
        self.direction = (direction[0] / length, direction[1] / length); self.damage = damage
        self.show(); self.draw()

    def update(self, dt: float) -> None:
        self.x += self.direction[0] * self.speed * dt; self.y += self.direction[1] * self.speed * dt; self.draw()
