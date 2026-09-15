"""Controllable combat robot."""
from __future__ import annotations
import math, turtle
from Core.Entity import Entity


class RobotPlayer(Entity):
    """Blue player robot with health, energy, cooldowns and temporary boosts."""
    def __init__(self, screen: turtle.Screen) -> None:
        super().__init__(screen, "square", "#278fe6", 30, 30)
        self.max_hp=100.; self.max_energy=100.; self.base_damage=20.; self.speed=180.
        self.hp=self.energy=100.; self.fire_cooldown=self.special_cooldown=0.; self.invincibility_timer=0.
        self.damage_boost_timer=self.speed_boost_timer=self.shield_timer=0.; self.last_direction=(0.,1.)
    @property
    def invincible(self) -> bool: return self.invincibility_timer>0 or self.shield_timer>0
    @property
    def current_damage(self) -> float: return self.base_damage*(1.5 if self.damage_boost_timer>0 else 1)
    def move(self, dx: float, dy: float, dt: float, obstacles: list[Entity], bounds: tuple[int,int,int,int]) -> None:
        if dx or dy:
            length=math.hypot(dx,dy); dx,dy=dx/length,dy/length; self.last_direction=(dx,dy)
            speed=self.speed*(1.3 if self.speed_boost_timer>0 else 1); self.move_with_obstacles(dx*speed*dt,dy*speed*dt,obstacles,bounds)
            self.turtle.setheading(math.degrees(math.atan2(dy,dx))-90)
    def shoot(self) -> bool:
        if self.fire_cooldown<=0: self.fire_cooldown=.18; self.turtle.color("#a7f4ff"); return True
        return False
    def use_special_attack(self) -> bool:
        if self.special_cooldown<=0 and self.energy>=30: self.energy-=30; self.special_cooldown=5; return True
        return False
    def take_damage(self, damage: float) -> bool:
        if self.invincible: return False
        self.hp=max(0,self.hp-damage); self.invincibility_timer=1.; self.turtle.color("white"); return self.hp<=0
    def heal(self, value: float) -> None: self.hp=min(self.max_hp,self.hp+value)
    def restore_energy(self, value: float) -> None: self.energy=min(self.max_energy,self.energy+value)
    def update(self, dt: float) -> None:
        self.energy=min(self.max_energy,self.energy+7*dt); self.fire_cooldown=max(0,self.fire_cooldown-dt); self.special_cooldown=max(0,self.special_cooldown-dt)
        for attr in ("invincibility_timer","damage_boost_timer","speed_boost_timer","shield_timer"): setattr(self,attr,max(0,getattr(self,attr)-dt))
        self.turtle.color("#278fe6" if self.invincibility_timer<=0 or int(self.invincibility_timer*12)%2 else "#b9efff"); self.draw()
    def reset(self) -> None:
        self.x,self.y=0.,-150.; self.hp=self.max_hp; self.energy=self.max_energy; self.fire_cooldown=self.special_cooldown=0.; self.invincibility_timer=0.; self.damage_boost_timer=self.speed_boost_timer=self.shield_timer=0.; self.last_direction=(0.,1.); self.show(); self.draw()
