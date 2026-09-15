"""Pooled turtle-circle explosion."""
from __future__ import annotations
import turtle
from Core.Entity import Entity
class Explosion(Entity):
    """Short expanding orange hit/destroy effect."""
    def __init__(self,screen:turtle.Screen)->None: super().__init__(screen,"circle","#ffba42",10,10); self.life=0.; self.max_life=.38
    def activate(self,x:float,y:float)->None: self.x,self.y=x,y; self.life=self.max_life; self.show(); self.draw()
    def update(self,dt:float)->None:
        self.life-=dt; scale=1+(1-self.life/self.max_life)*3; self.turtle.shapesize(scale,scale); self.turtle.color("#fff0a0" if self.life>.15 else "#ff7043"); self.draw()
