import pygame as pg
import sys

from levels import ChargeLevels, Level1, Level2, Level3
from player import Player
from enemy import Enemy
from settings import ANCHO, ALTO, TILE_SIZE, FPS

class Game:
    def __init__(self):
        pg.init()

        self.ancho, self.alto = ANCHO, ALTO
        self.IndexAncho, self.IndexAlto = round(self.ancho/ANCHO, 2), round(self.alto/ALTO, 2)
        self.tile_size = TILE_SIZE * self.IndexAlto

        self.screen = pg.display.set_mode((self.ancho, self.alto), pg.RESIZABLE)
        self.clock = pg.time.Clock()
        self.delta_time = 1

        self.camera_x = 0
        self.camera_y = 0

        self.projectiles = pg.sprite.Group()

        self.Recharge()
    
    def Recharge(self):
        self.Level = ChargeLevels(self, Level1)
        self.player = Player(self)

        self.enemy_list = []
        for pos in self.Level.enemy1_pos:
            self.enemy_list.append(Enemy(self, (pos[0], pos[1])))
    
    def update_camera(self):
        scale = TILE_SIZE * self.IndexAlto
        self.camera_x = self.player.x * scale - ANCHO / 2
        self.camera_y = self.player.y * scale - ALTO / 2

    def update(self):
        self.player.update()
        self.projectiles.update()

        for enemy in self.enemy_list:
            enemy.update()

        self.update_camera()

        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f"Gameplay - FPS: {self.clock.get_fps():.1f}")

    def draw(self):
        self.screen.fill('black')
        self.Level.draw()
        self.player.draw()
        
        # Dibujar proyectiles manualmente con cámara
        for proj in self.projectiles:
            proj.draw(self.screen, self.camera_x, self.camera_y)
        
        for enemy in self.enemy_list:
            enemy.draw()

    def check_events(self):
        hit_tiempo_actual = pg.time.get_ticks()
        hand_tiempo_actual = pg.time.get_ticks()

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

            elif event.type == pg.VIDEORESIZE:
                self.ancho, self.alto = event.w, event.h
                self.screen = pg.display.set_mode((self.ancho, self.alto), pg.RESIZABLE)
                self.IndexAncho, self.IndexAlto = self.ancho/ANCHO, self.alto/ALTO
                self.Recharge()
            
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.player.sttas['hand'] == 0:
                    self.player.hand_visible = True
                    self.player.time_hand = hand_tiempo_actual
                    
                    for enemy in self.enemy_list:
                        if self.player.rect_hand_world.colliderect(enemy.rect):
                            enemy.sttas["life"] -= 1
                            if enemy.sttas["life"] < 1:
                                self.enemy_list.remove(enemy)

                if self.player.sttas['hand'] == 1:
                    self.player.shoot()
            
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
                self.player.hit_visible = True
                self.player.time_hit = hit_tiempo_actual
        
        if self.player.hit_visible and (hit_tiempo_actual - self.player.time_hit >= self.player.hit_ms):
            self.player.hit_visible = False
        
        if self.player.hand_visible and (hand_tiempo_actual - self.player.time_hand >= self.player.hand_ms):
            self.player.hand_visible = False

    def run(self):
        while True:
            self.update()
            self.check_events()
            self.draw()