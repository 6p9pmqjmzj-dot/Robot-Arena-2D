"""Enemy energy bolt."""
from __future__ import annotations
import turtle
from Projectiles.Projectile import Projectile
class EnemyProjectile(Projectile):
    """Orange-red shot fired by ShooterBots."""
    def __init__(self, screen: turtle.Screen) -> None:
        super().__init__(screen, "#ff7554"); self.speed = 300; self.owner = "enemy"
