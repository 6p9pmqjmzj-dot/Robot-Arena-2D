"""Player energy bolt."""
from __future__ import annotations
import turtle
from Projectiles.Projectile import Projectile
class PlayerProjectile(Projectile):
    """Fast cyan shot owned by the player."""
    def __init__(self, screen: turtle.Screen) -> None:
        super().__init__(screen, "#49eaff"); self.speed = 520; self.owner = "player"
