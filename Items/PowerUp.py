"""Base collectible object."""
from __future__ import annotations
import turtle
from Core.Entity import Entity
class PowerUp(Entity):
    """Timed collectible used by the shared item pool."""
    def __init__(self, screen: turtle.Screen, color: str, kind: str) -> None:
        super().__init__(screen,"circle",color,20,20); self.kind=kind; self.life=0.
    def activate(self,x:float,y:float) -> None: self.x,self.y=x,y; self.life=12; self.show(); self.draw()
    def update(self,dt:float)->None: self.life-=dt; self.turtle.shapesize(1+(.1 if int(self.life*4)%2 else 0),1+(.1 if int(self.life*4)%2 else 0))
