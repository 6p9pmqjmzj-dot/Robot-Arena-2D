"""Robot Arena game coordinator."""
from __future__ import annotations
import math
import time
from pathlib import Path
import turtle
from Core.Collision import check_collision
from Core.HUD import HUD
from Core.InputManager import InputManager
from Core.ObjectPool import ObjectPool
from Environment.Arena import Arena
from Player.RobotPlayer import RobotPlayer
from Enemies.EnemyManager import EnemyManager
from Projectiles.ProjectileManager import ProjectileManager
from Items.PowerUp import PowerUp
from Items.HealthPack import HealthPack
from Items.EnergyCell import EnergyCell
from Items.DamageBoost import DamageBoost
from Items.SpeedBoost import SpeedBoost
from Items.ShieldPowerUp import ShieldPowerUp
from Effects.Explosion import Explosion


class Game:
    """Owns game state and advances it through turtle's non-blocking timer."""
    FPS = 60
    def __init__(self) -> None:
        self.screen=turtle.Screen(); self.screen.title("Robot Arena"); self.screen.setup(1040,680); self.screen.tracer(0,0)
        self.arena=Arena(self.screen); self.input=InputManager(self.screen); self.player=RobotPlayer(self.screen)
        self.enemies=EnemyManager(self.screen); self.projectiles=ProjectileManager(self.screen); self.hud=HUD(self.screen)
        self.item_pools={"health":ObjectPool(lambda:HealthPack(self.screen),2),"energy":ObjectPool(lambda:EnergyCell(self.screen),2),"damage":ObjectPool(lambda:DamageBoost(self.screen),1),"speed":ObjectPool(lambda:SpeedBoost(self.screen),1),"shield":ObjectPool(lambda:ShieldPowerUp(self.screen),1)}
        self.explosions=ObjectPool(lambda:Explosion(self.screen),8)
        self.highscore_path=Path(__file__).with_name("highscore.txt"); self.high_score=self._load_high_score()
        self.score=0; self.level=1; self.elapsed=0.; self.combo=0; self.combo_timer=0.; self.item_timer=7.; self.paused=False; self.game_over=False; self.running=True; self.last_clock=0.; self.message_until=0.
        self.screen.onkeypress(self._shoot,"space"); self.screen.onkeypress(self._special,"e"); self.screen.onkeypress(self.toggle_pause,"p"); self.screen.onkeypress(self.restart,"r"); self.screen.onkeypress(self.quit,"q"); self.screen.listen()
        self.restart(); self.screen.ontimer(self.loop,0)

    def _load_high_score(self) -> int:
        try: return int(self.highscore_path.read_text(encoding="utf-8").strip())
        except (OSError, ValueError): return 0
    def _save_high_score(self) -> None:
        try: self.highscore_path.write_text(str(self.high_score),encoding="utf-8")
        except OSError: pass
    def _items(self) -> list[PowerUp]: return [item for pool in self.item_pools.values() for item in pool.in_use]
    def _message(self,text:str,seconds:float=2,color:str="#7eeaff") -> None:
        self.hud.show_message(text,color); self.message_until=self.elapsed+seconds
    def _shoot(self) -> None:
        if not self.paused and not self.game_over and self.player.shoot():
            x,y=self.player.last_direction; self.projectiles.fire_player(self.player.x+x*22,self.player.y+y*22,(x,y),self.player.current_damage)
    def _special(self) -> None:
        if self.paused or self.game_over or not self.player.use_special_attack(): return
        self.explosions.get().activate(self.player.x,self.player.y)
        for enemy in self.enemies.enemies[:]:
            if math.hypot(enemy.x-self.player.x,enemy.y-self.player.y)<=120 and enemy.take_damage(55): self._kill_enemy(enemy)
    def toggle_pause(self) -> None:
        if self.game_over:return
        self.paused=not self.paused
        if self.paused:self.hud.show_message("PAUSED\nPress P to resume","#ffd75b")
        else:self.hud.clear_message()
    def quit(self) -> None:
        self.running=False
        try:self.screen.bye()
        except turtle.Terminator:pass
    def restart(self) -> None:
        self.enemies.clear();self.projectiles.clear();self.explosions.clear()
        for pool in self.item_pools.values():pool.clear()
        self.player.reset();self.score=0;self.level=1;self.elapsed=0.;self.combo=0;self.combo_timer=0.;self.item_timer=6.;self.paused=False;self.game_over=False;self.enemies.spawn_timer=1.2;self.hud.clear_message()
    def _kill_enemy(self,enemy:object) -> None:
        # Enemy object is intentionally kept generic for concise collision dispatch.
        value=int(getattr(enemy,"score_value")); self.combo=self.combo+1 if self.combo_timer>0 else 1; self.combo_timer=3
        self.score+=value*self.combo; self.explosions.get().activate(float(getattr(enemy,"x")),float(getattr(enemy,"y"))); self.enemies.release(enemy)  # type: ignore[arg-type]
    def _spawn_item(self) -> None:
        import random
        kind=random.choice(list(self.item_pools)); item=self.item_pools[kind].get()
        item.activate(random.randint(-390,390),random.randint(-190,190))
    def _update_collisions(self) -> None:
        for shot in self.projectiles.player[:]:
            for enemy in self.enemies.enemies[:]:
                if check_collision(shot,enemy):
                    self.projectiles.player_pool.release(shot)
                    if enemy.take_damage(shot.damage):self._kill_enemy(enemy)
                    break
        for shot in self.projectiles.enemy[:]:
            if check_collision(shot,self.player): self.projectiles.enemy_pool.release(shot); self.player.take_damage(shot.damage)
        for enemy in self.enemies.enemies[:]:
            if check_collision(enemy,self.player) and enemy.contact_cooldown<=0:
                self.player.take_damage(enemy.damage); enemy.contact_cooldown=.9
                enemy.x+=(enemy.x-self.player.x)*.3; enemy.y+=(enemy.y-self.player.y)*.3; enemy.draw()
        for item in self._items()[:]:
            if check_collision(item,self.player):
                if item.kind=="health":self.player.heal(25)
                elif item.kind=="energy":self.player.restore_energy(30)
                elif item.kind=="damage":self.player.damage_boost_timer=8
                elif item.kind=="speed":self.player.speed_boost_timer=6
                else:self.player.shield_timer=5
                self.item_pools[item.kind].release(item)
    def _update_effects(self,dt:float) -> None:
        for effect in self.explosions.in_use[:]:
            effect.update(dt)
            if effect.life<=0:self.explosions.release(effect)
        for item in self._items()[:]:
            item.update(dt)
            if item.life<=0:self.item_pools[item.kind].release(item)
    def _end_game(self) -> None:
        self.game_over=True
        if self.score>self.high_score:self.high_score=self.score;self._save_high_score(); headline="NEW HIGH SCORE!\n"
        else:headline=""
        self.hud.show_message(f"{headline}GAME OVER\nFINAL SCORE: {self.score}\nHIGH SCORE: {self.high_score}\nPress R to restart\nPress Q to quit","#ff886f")
    def loop(self) -> None:
        if not self.running:return
        try:
            now=time.perf_counter()
            dt=min(.05, now-self.last_clock) if self.last_clock else 1/self.FPS;self.last_clock=now
            if not self.paused and not self.game_over:
                self.elapsed+=dt; self.score+=int(dt); new_level=int(self.elapsed//30)+1
                if new_level>self.level:self.level=new_level;self.score+=500;self._message("LEVEL UP!",2,"#ffe15c")
                dx,dy=self.input.direction();self.player.move(dx,dy,dt,self.arena.obstacles,self.arena.bounds);self.player.update(dt)
                shooters=self.enemies.update(dt,self.player.x,self.player.y,self.level,self.arena.bounds)
                for shooter in shooters:self.projectiles.fire_enemy(shooter.x,shooter.y,(self.player.x-shooter.x,self.player.y-shooter.y),shooter.damage)
                self.projectiles.update(dt,self.arena.bounds);self._update_collisions();self._update_effects(dt);self.combo_timer=max(0,self.combo_timer-dt)
                if self.combo_timer<=0:self.combo=0
                self.item_timer-=dt
                if self.item_timer<=0:self._spawn_item();self.item_timer=9
                if self.player.hp<=0:self._end_game()
                if self.message_until and self.elapsed>=self.message_until:self.hud.clear_message();self.message_until=0
            self.hud.update(self.score,self.high_score,self.level,self.player.hp,self.player.energy,self.player.shield_timer,self.combo);self.screen.update();self.screen.ontimer(self.loop,1000//self.FPS)
        except turtle.Terminator:self.running=False
