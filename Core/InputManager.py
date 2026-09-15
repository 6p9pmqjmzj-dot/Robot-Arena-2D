"""Keyboard state tracking compatible with turtle events."""
from __future__ import annotations
import turtle


class InputManager:
    """Tracks held movement keys and dispatches one-shot actions."""
    def __init__(self, screen: turtle.Screen) -> None:
        self.pressed: set[str] = set(); self.screen = screen
        for key in ("w", "a", "s", "d", "Up", "Down", "Left", "Right"):
            screen.onkeypress(lambda k=key: self.pressed.add(k), key)
            screen.onkeyrelease(lambda k=key: self.pressed.discard(k), key)

    def direction(self) -> tuple[float, float]:
        x = float(("d" in self.pressed or "Right" in self.pressed) - ("a" in self.pressed or "Left" in self.pressed))
        y = float(("w" in self.pressed or "Up" in self.pressed) - ("s" in self.pressed or "Down" in self.pressed))
        return x, y
