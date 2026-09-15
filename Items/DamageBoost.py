from __future__ import annotations
import turtle
from Items.PowerUp import PowerUp
class DamageBoost(PowerUp):
    """Temporarily increases bolt damage."""
    def __init__(self,screen:turtle.Screen)->None: super().__init__(screen,"#ffd75b","damage")
