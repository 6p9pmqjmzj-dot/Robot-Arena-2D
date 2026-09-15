"""Fast enemy robot."""
from __future__ import annotations
import math, random, turtle
from Enemies.Enemy import Enemy
class FastBot(Enemy):
    """Small orange chaser with a light evasive wobble."""
    def __init__(self, screen: turtle.Screen) -> None: super().__init__(screen, "#ff9d3d", 18, 18); self.enemy_type = "FastBot"
    def configure(self, level: int) -> None:
        self.max_hp = self.hp = 30 + (level - 1) * 3; self.speed = 105 + level * 4; self.damage = 8; self.score_value = 150
    def update_ai(self, dt: float, px: float, py: float) -> None:
        dx, dy = px-self.x, py-self.y; angle = math.atan2(dy, dx) + random.uniform(-0.32, .32)
        self.x += math.cos(angle)*self.speed*dt; self.y += math.sin(angle)*self.speed*dt
        self.contact_cooldown=max(0,self.contact_cooldown-dt); self.draw()
