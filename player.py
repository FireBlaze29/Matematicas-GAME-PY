from settings import *
import pygame as pg
import math

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
    
    def movement(self):
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dy -= speed
        if keys[pg.K_s]:
            dy += speed
        if keys[pg.K_a]:
            dx -= speed
        if keys[pg.K_d]:
            dx += speed

        if dx != 0 and dy != 0:
            dx *= 0.7071  # 1 / sqrt(2)
            dy *= 0.7071

        self.check_wall_collision(dx, dy)

        self.rotate_toward_mouse()

    def rotate_toward_mouse(self):
        
        mouse_px, mouse_py = pg.mouse.get_pos()
        
        scale = TILE_SIZE * self.game.IndexAlto
        world_mouse_x = mouse_px / scale
        world_mouse_y = mouse_py / scale
        
        dx = world_mouse_x - self.x
        dy = world_mouse_y - self.y
        self.angle = math.atan2(dy, dx)

        self.angle %= math.tau #tau es 2*pi, esto asegura que el ángulo siempre esté entre 0 y 2*pi
    
    def check_wall(self, x, y):
        return (x, y) not in self.game.Level.world_map
    
    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy)):
            self.y += dy
    
    def draw(self):
        pg.draw.line(self.game.screen, 'yellow', (self.x * TILE_SIZE * self.game.IndexAlto, self.y * TILE_SIZE * self.game.IndexAlto),
                     (self.x * TILE_SIZE * self.game.IndexAlto + ANCHO * math.cos(self.angle),
                      self.y * TILE_SIZE * self.game.IndexAlto + ANCHO * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'yellow', (self.x * TILE_SIZE * self.game.IndexAlto, self.y * TILE_SIZE * self.game.IndexAlto), 5)

    def update(self):
        self.movement()
    
    @property
    def pos(self):
        return (self.x, self.y)
    
    @property
    def map_pos(self):
        return int(self.x), int(self.y)