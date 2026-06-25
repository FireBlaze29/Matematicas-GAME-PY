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

        size = int(self.radius * 2 * self.game.tile_size)
        self.image = pg.Surface((size, size), pg.SRCALPHA)
        pg.draw.circle(self.image, (255, 255, 255), (size//2, size//2), size//2)
        
        self.rect = self.image.get_rect(center=(x * self.game.tile_size,
                                                y * self.game.tile_size))

    def update(self):
        dx = math.cos(self.angle) * self.speed * self.game.delta_time
        dy = math.sin(self.angle) * self.speed * self.game.delta_time
        self.x += dx
        self.y += dy

        if self.game.player.check_circle_collision(self.x, self.y, self.radius):
            self.kill()


        self.rect.center = (self.x * self.game.tile_size,
                            self.y * self.game.tile_size)

    def draw(self, screen, camera_x, camera_y):
        
        
        screen_x = self.rect.centerx - camera_x
        screen_y = self.rect.centery - camera_y
        
        rect_pantalla = self.image.get_rect(center=(screen_x, screen_y))
        screen.blit(self.image, rect_pantalla)