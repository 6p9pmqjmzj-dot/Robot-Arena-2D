from __future__ import annotations
import turtle
from Items.PowerUp import PowerUp
class EnergyCell(PowerUp):
    """Restores energy."""
    def __init__(self,screen:turtle.Screen)->None: super().__init__(screen,"#56dff5","energy")
