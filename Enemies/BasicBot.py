"""Basic enemy robot."""
from __future__ import annotations
import turtle
from Enemies.Enemy import Enemy
class BasicBot(Enemy):
    """Balanced red chaser."""
    def __init__(self, screen: turtle.Screen) -> None: super().__init__(screen, "#e04d50", 26, 26); self.enemy_type = "BasicBot"
    def configure(self, level: int) -> None:
        self.max_hp = self.hp = 50 + (level - 1) * 4; self.speed = 62 + level * 3; self.damage = 10; self.score_value = 100
