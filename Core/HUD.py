"""Fixed heads-up display."""
from __future__ import annotations
import turtle


class HUD:
    """Renders score, bars, timers and center messages."""
    def __init__(self, screen: turtle.Screen) -> None:
        self.writer = turtle.Turtle(visible=False); self.writer.penup(); self.writer.color("white")
        self.message = turtle.Turtle(visible=False); self.message.penup(); self.message.color("#7eeaff")
        self.screen = screen

    def update(self, score: int, high: int, level: int, hp: float, energy: float,
               shield: float, combo: int) -> None:
        self.writer.clear(); self.writer.goto(-470, 305)
        bar = lambda value: "#" * int(max(0, value) / 10) + "-" * (10 - int(max(0, value) / 10))
        lines = [f"SCORE: {score:06d}    HIGH SCORE: {high:06d}    LEVEL: {level}",
                 f"HP:     [{bar(hp)}] {int(hp):3d}", f"ENERGY: [{bar(energy)}] {int(energy):3d}"]
        if shield > 0: lines.append(f"SHIELD: {shield:.1f}s")
        if combo > 1: lines.append(f"COMBO: x{combo}")
        self.writer.write("\n".join(lines), align="left", font=("Arial", 12, "bold"))

    def show_message(self, text: str, color: str = "#7eeaff") -> None:
        self.message.clear(); self.message.color(color); self.message.goto(0, 20)
        self.message.write(text, align="center", font=("Arial", 24, "bold"))

    def clear_message(self) -> None: self.message.clear()
