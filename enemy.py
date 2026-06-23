from settings import *
import pygame as pg
import math

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, pos):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.x, self.y = pos[0], pos[1]
        self.angle = PLAYER_ANGLE
        self.radius = PLAYER_RADIUS

        self.rect = pg.Rect(0, 0, self.radius * 2 * TILE_SIZE * self.game.IndexAlto,
                            self.radius * 2 * TILE_SIZE * self.game.IndexAlto)
        self.rect.center = (self.x * TILE_SIZE * self.game.IndexAlto,
                            self.y * TILE_SIZE * self.game.IndexAlto)
        
        self.sttas = {
            'life': 5,
            'hand': 0,
            'obj': None,
        }

        
    def movement(self):
        pass

    def check_circle_collision(self, cx, cy, radius):

        min_tile_x = int(math.floor(cx - radius))
        max_tile_x = int(math.ceil(cx + radius))
        min_tile_y = int(math.floor(cy - radius))
        max_tile_y = int(math.ceil(cy + radius))

        for y in range(min_tile_y, max_tile_y + 1):
            for x in range(min_tile_x, max_tile_x + 1):
                if (x, y) in self.game.Level.world_map:
                    closest_x = max(x, min(cx, x + 1))
                    closest_y = max(y, min(cy, y + 1))
                    dist_x = cx - closest_x
                    dist_y = cy - closest_y
                    if dist_x * dist_x + dist_y * dist_y < radius * radius:
                        return True
        return False
    
    def draw(self):
        pg.draw.line(self.game.screen, 'yellow',
                     (self.x * TILE_SIZE * self.game.IndexAlto, self.y * TILE_SIZE * self.game.IndexAlto),
                     (self.x * TILE_SIZE * self.game.IndexAlto + 12 * math.cos(self.angle),
                      self.y * TILE_SIZE * self.game.IndexAlto + 12 * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'yellow',
                       (self.x * TILE_SIZE * self.game.IndexAlto, self.y * TILE_SIZE * self.game.IndexAlto), 5)
        
        pg.draw.circle(self.game.screen, 'red',
                       (self.x * TILE_SIZE * self.game.IndexAlto, self.y * TILE_SIZE * self.game.IndexAlto),
                       self.radius * TILE_SIZE * self.game.IndexAlto, 2)
    
    def update(self):
        self.movement()