"""Shared hostile robot behaviour."""
from __future__ import annotations
import math
import turtle
from Core.Entity import Entity


class Enemy(Entity):
    """Base class for poolable hostile robots."""
    def __init__(self, screen: turtle.Screen, color: str, width: int, height: int) -> None:
        super().__init__(screen, "square", color, width, height)
        self.hp = self.max_hp = self.speed = self.damage = self.score_value = 0.0
        self.enemy_type = "Enemy"; self.contact_cooldown = 0.0; self.fire_timer = 0.0

    def configure(self, level: int) -> None: pass
    def activate(self, x: float, y: float, level: int) -> None:
        self.x, self.y = x, y; self.configure(level); self.show(); self.draw()
    def take_damage(self, damage: float) -> bool:
        self.hp -= damage; self.turtle.color("white"); return self.hp <= 0
    def update_ai(self, dt: float, player_x: float, player_y: float) -> tuple[float, float] | None:
        """Move toward player; optional tuple signals an enemy shot direction."""
        dx, dy = player_x - self.x, player_y - self.y; length = math.hypot(dx, dy) or 1
        self.x += dx / length * self.speed * dt; self.y += dy / length * self.speed * dt
        self.contact_cooldown = max(0.0, self.contact_cooldown - dt); self.draw(); return None
    def reset(self) -> None:
        super().reset(); self.contact_cooldown = self.fire_timer = 0.0
