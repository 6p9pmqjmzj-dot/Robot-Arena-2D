"""Pooled player and enemy projectile control."""
from __future__ import annotations
import turtle
from Core.ObjectPool import ObjectPool
from Projectiles.PlayerProjectile import PlayerProjectile
from Projectiles.EnemyProjectile import EnemyProjectile


class ProjectileManager:
    """Creates no turtle during normal projectile gameplay after warm-up."""
    def __init__(self, screen: turtle.Screen) -> None:
        self.player_pool = ObjectPool(lambda: PlayerProjectile(screen), 18)
        self.enemy_pool = ObjectPool(lambda: EnemyProjectile(screen), 12)

    @property
    def player(self) -> list[PlayerProjectile]: return self.player_pool.in_use
    @property
    def enemy(self) -> list[EnemyProjectile]: return self.enemy_pool.in_use
    def fire_player(self, x: float, y: float, direction: tuple[float, float], damage: float) -> None:
        self.player_pool.get().activate(x, y, direction, damage)
    def fire_enemy(self, x: float, y: float, direction: tuple[float, float], damage: float) -> None:
        self.enemy_pool.get().activate(x, y, direction, damage)
    def update(self, dt: float, bounds: tuple[int, int, int, int]) -> None:
        left, right, bottom, top = bounds
        for pool in (self.player_pool, self.enemy_pool):
            for shot in pool.in_use[:]:
                shot.update(dt)
                if not (left <= shot.x <= right and bottom <= shot.y <= top): pool.release(shot)
    def clear(self) -> None: self.player_pool.clear(); self.enemy_pool.clear()
