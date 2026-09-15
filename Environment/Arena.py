"""Arena geometry and background."""
from __future__ import annotations
import turtle
from Environment.ArenaDecoration import ArenaDecoration
from Environment.Obstacle import Obstacle


class Arena:
    """Owns world bounds and a few safe, fixed obstacles."""
    left, right, bottom, top = -480, 480, -280, 270
    def __init__(self, screen: turtle.Screen) -> None:
        self.screen = screen; screen.bgcolor("#10161b")
        border = turtle.Turtle(visible=False); border.penup(); border.color("#5f7988"); border.pensize(4)
        border.goto(self.left, self.bottom); border.pendown()
        for point in ((self.right, self.bottom), (self.right, self.top), (self.left, self.top), (self.left, self.bottom)):
            border.goto(*point)
        ArenaDecoration(self.left, self.right, self.bottom, self.top).draw()
        self.obstacles = [Obstacle(screen, -155, 70, 90, 34), Obstacle(screen, 180, -85, 110, 34),
                          Obstacle(screen, 15, 150, 60, 30)]

    @property
    def bounds(self) -> tuple[int, int, int, int]: return self.left, self.right, self.bottom, self.top
