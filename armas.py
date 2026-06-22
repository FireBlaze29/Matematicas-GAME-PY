import pygame as pg
import math
from settings import TILE_SIZE

class Armas(pg.sprite.Sprite):
    def __init__(self, game, x, y, angle):
        super().__init__()
        self.game = game
        self.x, self.y = x, y
        self.angle = angle
        self.speed = 0.02
        self.radius = 0.4

        size = int(self.radius * 2 * TILE_SIZE * self.game.IndexAlto)
        self.image = pg.Surface((size, size), pg.SRCALPHA)
        pg.draw.circle(self.image, (255, 255, 255), (size//2, size//2), size//2)
        self.rect = self.image.get_rect(center=(x * TILE_SIZE * self.game.IndexAlto,
                                                y * TILE_SIZE * self.game.IndexAlto))

    def update(self):

        dx = math.cos(self.angle) * self.speed * self.game.delta_time
        dy = math.sin(self.angle) * self.speed * self.game.delta_time
        self.x += dx
        self.y += dy

        if self.game.player.check_circle_collision(self.x, self.y, self.radius):
            self.kill()   # eliminar proyectil

        # Actualizar rect
        self.rect.center = (self.x * TILE_SIZE * self.game.IndexAlto,
                            self.y * TILE_SIZE * self.game.IndexAlto)