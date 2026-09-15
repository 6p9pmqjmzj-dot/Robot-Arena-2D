"""Enemy spawning, AI and pooling."""
from __future__ import annotations
import random, turtle
from Core.ObjectPool import ObjectPool
from Enemies.Enemy import Enemy
from Enemies.BasicBot import BasicBot
from Enemies.FastBot import FastBot
from Enemies.ShooterBot import ShooterBot
from Enemies.TankBot import TankBot


class EnemyManager:
    """Spawns permitted types by level and caps active robots."""
    def __init__(self, screen: turtle.Screen) -> None:
        self.screen=screen; self.pools={"BasicBot":ObjectPool(lambda:BasicBot(screen),8), "FastBot":ObjectPool(lambda:FastBot(screen),5), "ShooterBot":ObjectPool(lambda:ShooterBot(screen),4), "TankBot":ObjectPool(lambda:TankBot(screen),3)}
        self.spawn_timer=1.2
    @property
    def enemies(self) -> list[Enemy]: return [e for p in self.pools.values() for e in p.in_use]
    def update(self, dt: float, px: float, py: float, level: int, bounds: tuple[int,int,int,int]) -> list[Enemy]:
        self.spawn_timer-=dt
        if self.spawn_timer<=0 and len(self.enemies)<min(8+level*2,24): self.spawn(level,bounds); self.spawn_timer=max(.36,1.35-level*.09)
        shooters=[]
        for enemy in self.enemies:
            result=enemy.update_ai(dt,px,py)
            if result: shooters.append(enemy)
        return shooters
    def spawn(self, level: int, b: tuple[int,int,int,int]) -> None:
        choices=["BasicBot"] + (["FastBot"] if level>=2 else []) + (["ShooterBot"] if level>=3 else []) + (["TankBot"] if level>=4 else [])
        kind=random.choice(choices); left,right,bottom,top=b; side=random.randrange(4)
        x,y=(random.randint(left,right),top-15) if side==0 else ((random.randint(left,right),bottom+15) if side==1 else ((right-15,random.randint(bottom,top)) if side==2 else (left+15,random.randint(bottom,top))))
        self.pools[kind].get().activate(x,y,level)
    def release(self, enemy: Enemy) -> None: self.pools[enemy.enemy_type].release(enemy)
    def clear(self) -> None:
        for pool in self.pools.values(): pool.clear()
