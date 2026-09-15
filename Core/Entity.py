"""Base drawable entity for the arena."""
from __future__ import annotations
import turtle
from typing import TYPE_CHECKING
from Core.Collision import check_collision

if TYPE_CHECKING:
    from Environment.Obstacle import Obstacle


class Entity:
    """A pooled turtle-backed object with simple rectangular bounds."""
    def __init__(self, canvas: turtle.Screen, shape: str = "square", color: str = "white",
                 width: float = 20, height: float = 20) -> None:
        self.canvas, self.width, self.height = canvas, width, height
        self.x = self.y = self.vx = self.vy = 0.0
        self.active = self.visible = False
        self.turtle = turtle.Turtle(visible=False)
        self.turtle.penup(); self.turtle.shape(shape); self.turtle.color(color)
        self.turtle.shapesize(stretch_wid=height / 20, stretch_len=width / 20)

    def update(self, dt: float) -> None:
        """Advance using velocity."""
        self.x += self.vx * dt; self.y += self.vy * dt; self.draw()

    def draw(self) -> None:
        """Synchronize the turtle's position."""
        if self.active:
            self.turtle.goto(self.x, self.y)

    def show(self) -> None:
        self.active = self.visible = True; self.turtle.showturtle()

    def hide(self) -> None:
        self.visible = False; self.turtle.hideturtle()

    def reset(self) -> None:
        """Put the entity into its safe pooled state."""
        self.active = False; self.vx = self.vy = 0.0; self.hide()

    def get_bounds(self) -> tuple[float, float, float, float]:
        return (self.x - self.width / 2, self.y - self.height / 2,
                self.x + self.width / 2, self.y + self.height / 2)

    def collides_with(self, other: "Entity") -> bool:
        return check_collision(self, other)

    def move_with_obstacles(self, dx: float, dy: float, obstacles: list["Obstacle"],
                            bounds: tuple[float, float, float, float]) -> None:
        """Move one axis at a time, stopping on arena obstacles."""
        left, right, bottom, top = bounds
        old_x = self.x; self.x = max(left + self.width / 2, min(right - self.width / 2, self.x + dx))
        if any(self.collides_with(o) for o in obstacles): self.x = old_x
        old_y = self.y; self.y = max(bottom + self.height / 2, min(top - self.height / 2, self.y + dy))
        if any(self.collides_with(o) for o in obstacles): self.y = old_y
        self.draw()
