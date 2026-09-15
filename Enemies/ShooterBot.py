"""Ranged enemy robot."""
from __future__ import annotations
import math, turtle
from Enemies.Enemy import Enemy
class ShooterBot(Enemy):
    """Purple robot that maintains range and reports shots to its manager."""
    def __init__(self, screen: turtle.Screen) -> None: super().__init__(screen, "#b46be8", 30, 30); self.enemy_type = "ShooterBot"
    def configure(self, level: int) -> None:
        self.max_hp=self.hp=70+(level-1)*5; self.speed=58+level*2; self.damage=12; self.score_value=250; self.fire_timer=1.2
    def update_ai(self, dt: float, px: float, py: float) -> tuple[float,float] | None:
        dx,dy=px-self.x,py-self.y; dist=math.hypot(dx,dy) or 1; nx,ny=dx/dist,dy/dist
        movement = -1 if dist < 155 else (1 if dist > 210 else 0)
        self.x += (nx*movement - ny*.35)*self.speed*dt; self.y += (ny*movement + nx*.35)*self.speed*dt
        self.fire_timer-=dt; self.contact_cooldown=max(0,self.contact_cooldown-dt); self.draw()
        if 115 < dist < 250 and self.fire_timer <= 0: self.fire_timer=1.55; return nx,ny
        return None
