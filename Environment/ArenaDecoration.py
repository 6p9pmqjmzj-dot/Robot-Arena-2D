"""Non-interactive industrial arena drawing."""
from __future__ import annotations
import turtle


class ArenaDecoration:
    """Draws permanent grid, lights and warning markings once."""
    def __init__(self, left: int, right: int, bottom: int, top: int) -> None:
        self.pen = turtle.Turtle(visible=False); self.pen.penup(); self.pen.speed(0)
        self.left, self.right, self.bottom, self.top = left, right, bottom, top

    def draw(self) -> None:
        p = self.pen; p.color("#25313a"); p.pensize(1)
        for x in range(self.left, self.right + 1, 40):
            p.goto(x, self.bottom); p.pendown(); p.goto(x, self.top); p.penup()
        for y in range(self.bottom, self.top + 1, 40):
            p.goto(self.left, y); p.pendown(); p.goto(self.right, y); p.penup()
        p.color("#7f4e18"); p.pensize(3)
        for y in (self.bottom + 18, self.top - 18):
            for x in range(self.left + 20, self.right, 70):
                p.goto(x, y); p.pendown(); p.goto(x + 28, y); p.penup()
        p.color("#4ee8d2"); p.pensize(4)
        for x, y in ((self.left + 18, self.bottom + 18), (self.right - 18, self.bottom + 18),
                     (self.left + 18, self.top - 18), (self.right - 18, self.top - 18)):
            p.goto(x, y); p.dot(9)
