"""Armored enemy robot."""
from __future__ import annotations
import turtle
from Enemies.Enemy import Enemy
class TankBot(Enemy):
    """Large slow armored robot."""
    def __init__(self, screen: turtle.Screen) -> None: super().__init__(screen, "#8b9097", 42, 42); self.enemy_type = "TankBot"
    def configure(self, level: int) -> None:
        self.max_hp=self.hp=150+(level-1)*12; self.speed=37+level*2; self.damage=20; self.score_value=300
