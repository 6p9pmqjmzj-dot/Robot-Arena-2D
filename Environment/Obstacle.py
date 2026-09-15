"""Static collision block."""
from __future__ import annotations
import turtle
from Core.Entity import Entity


class Obstacle(Entity):
    """A non-active metal block used by movement collision."""
    def __init__(self, screen: turtle.Screen, x: float, y: float, width: float, height: float) -> None:
        super().__init__(screen, "square", "#39434d", width, height)
        self.x, self.y = x, y; self.active = True; self.show(); self.draw()
