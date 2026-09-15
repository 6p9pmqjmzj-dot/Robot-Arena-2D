from __future__ import annotations
import turtle
from Items.PowerUp import PowerUp
class HealthPack(PowerUp):
    """Restores health."""
    def __init__(self,screen:turtle.Screen)->None: super().__init__(screen,"#54df80","health")
