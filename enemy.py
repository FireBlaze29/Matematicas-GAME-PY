from settings import *
import pygame as pg
import math

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, pos):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.x, self.y = pos[0] + 0.5, pos[1] + 0.5  # Centrar en el tile
        self.angle = PLAYER_ANGLE
        self.radius = PLAYER_RADIUS
        self.speed = 0.01  # Velocidad de movimiento

        self.rect = pg.Rect(0, 0, self.radius * 2 * self.game.tile_size,
                            self.radius * 2 * self.game.tile_size)
        self.rect.center = (self.x * self.game.tile_size,
                            self.y * self.game.tile_size)
        
        self.sttas = {
            'life': 5,
            'hand': 0,
            'obj': None,
        }

    def movement(self):
        if not self.game.player:
            return

        # Calcular dirección hacia el jugador
        dx = self.game.player.x - self.x
        dy = self.game.player.y - self.y
        distance = math.hypot(dx, dy)
        
        # Actualizar ángulo para mirar al jugador
        self.angle = math.atan2(dy, dx)
        self.angle %= math.tau

        # Si está muy cerca, no moverse (evita solapamiento)
        if distance < 0.5:
            return

        # Normalizar dirección
        if distance > 0:
            dx /= distance
            dy /= distance

        # Velocidad ajustada por delta_time
        speed = self.speed * self.game.delta_time

        # Intentar mover en X
        new_x = self.x + dx * speed
        if not self.check_circle_collision(new_x, self.y, self.radius):
            self.x = new_x
        else:
            # Si no puede moverse en X, intenta moverse en Y con el mismo dx
            # pero solo si el movimiento en Y no causa colisión
            pass

        # Intentar mover en Y
        new_y = self.y + dy * speed
        if not self.check_circle_collision(self.x, new_y, self.radius):
            self.y = new_y

        # Actualizar rect
        self.rect.center = (self.x * self.game.tile_size,
                            self.y * self.game.tile_size)

    def check_circle_collision(self, cx, cy, radius):
        """Devuelve True si el círculo (cx, cy, radius) colisiona con alguna pared."""
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
        cam_x = self.game.camera_x
        cam_y = self.game.camera_y
        
        # Línea de dirección (hacia el jugador)
        pg.draw.line(self.game.screen, 'yellow',
                     (self.x * self.game.tile_size - cam_x,
                      self.y * self.game.tile_size - cam_y),
                     (self.x * self.game.tile_size - cam_x + 12 * math.cos(self.angle),
                      self.y * self.game.tile_size - cam_y + 12 * math.sin(self.angle)), 2)
        
        # Punto central
        pg.draw.circle(self.game.screen, 'yellow',
                       (self.x * self.game.tile_size - cam_x,
                        self.y * self.game.tile_size - cam_y), 5)
        
        # Círculo de colisión
        pg.draw.circle(self.game.screen, 'red',
                       (self.x * self.game.tile_size - cam_x,
                        self.y * self.game.tile_size - cam_y),
                       self.radius * self.game.tile_size, 2)
    
    def update(self):
        self.movement()