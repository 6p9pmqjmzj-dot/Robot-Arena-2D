from __future__ import annotations
import turtle
from Items.PowerUp import PowerUp
class ShieldPowerUp(PowerUp):
    """Temporarily prevents damage."""
    def __init__(self,screen:turtle.Screen)->None: super().__init__(screen,"#a6b8ff","shield")
