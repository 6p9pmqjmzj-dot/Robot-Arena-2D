from __future__ import annotations
import turtle
from Items.PowerUp import PowerUp
class SpeedBoost(PowerUp):
    """Temporarily increases travel speed."""
    def __init__(self,screen:turtle.Screen)->None: super().__init__(screen,"#f6a4ff","speed")
