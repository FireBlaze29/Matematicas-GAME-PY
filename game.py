import pygame as pg #pip install pygame-ce
import sys

from levels import ChargeLevels, Level1
from player import Player
from settings import ANCHO, ALTO, TILE_SIZE, FPS

class Game:
    def __init__(self):
        pg.init()

        self.ancho, self.alto = ANCHO, ALTO
        self.IndexAncho, self.IndexAlto = self.ancho/ANCHO, self.alto/ALTO
        self.tile_size = TILE_SIZE * self.IndexAlto

        self.screen = pg.display.set_mode((self.ancho, self.alto), pg.RESIZABLE)
        self.clock = pg.time.Clock()
        self.delta_time = 1

        self.Recharge()
    
    def Recharge(self):
        self.Level = ChargeLevels(self, Level1)
        self.player = Player(self)

    def update(self):
        self.player.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f"Gameplay - FPS: {self.clock.get_fps():.1f}")

    def draw(self):
        self.screen.fill('black')
        self.Level.draw()
        self.player.draw()
        
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.VIDEORESIZE:
                self.ancho, self.alto = event.w, event.h
                self.screen = pg.display.set_mode((self.ancho, self.alto), pg.RESIZABLE)
                self.IndexAncho, self.IndexAlto = self.ancho/ANCHO, self.alto/ALTO
                self.Recharge()

    def run(self):
        while True:
            self.check_events()
            self.draw()
            self.update()