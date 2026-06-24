from settings import *
import pygame as pg
import math
from armas import Armas

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.x, self.y = self.game.Level.player_pos[0] + (TILE_SIZE/30), self.game.Level.player_pos[1] + (TILE_SIZE/30)
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

        self.create_hit()
        self.create_hand()

        self.rect_hand_world = pg.Rect(0, 0, 0, 0)
        self.rect_hit_world = pg.Rect(0, 0, 0, 0)

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
            dx *= 0.7071
            dy *= 0.7071

        new_x = self.x + dx
        if not self.check_circle_collision(new_x, self.y, self.radius):
            self.x = new_x

        new_y = self.y + dy
        if not self.check_circle_collision(self.x, new_y, self.radius):
            self.y = new_y

        self.rect.center = (self.x * TILE_SIZE * self.game.IndexAlto,
                            self.y * TILE_SIZE * self.game.IndexAlto)
        
        if keys[pg.K_f] and self.check_item_collision("bool"):
            self.sttas['hand'] = 1
            item = self.check_item_collision("coord")
            self.type_arm = self.game.Level.not_wall[item]
            del self.game.Level.not_wall[item]
        
        if keys[pg.K_y] and self.sttas['hand'] != 0:
            self.sttas['hand'] = 0

        self.rotate_toward_mouse()

    def rotate_toward_mouse(self):
        mouse_px, mouse_py = pg.mouse.get_pos()
        scale = TILE_SIZE * self.game.IndexAlto
        world_mouse_x = (mouse_px + self.game.camera_x) / scale
        world_mouse_y = (mouse_py + self.game.camera_y) / scale

        dx = world_mouse_x - self.x
        dy = world_mouse_y - self.y
        self.angle = math.atan2(dy, dx)
        self.angle %= math.tau

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
    
    def check_item_collision(self, validate, add_radius=0):
        pickup_radius = self.radius + add_radius
        for (tx, ty) in list(self.game.Level.not_wall.keys()):
            obj_x = tx + 0.5
            obj_y = ty + 0.5
            dist = math.hypot(self.x - obj_x, self.y - obj_y)
            if dist < pickup_radius:
                if validate == "coord":
                    return (tx, ty)
                elif validate == "bool":
                    return True

    def update_hitboxes(self):
        """Actualiza las superficies rotadas y los rectángulos en coordenadas de mundo."""
        # Rotar superficies con el ángulo actual
        self.roteted_hand = pg.transform.rotate(self.collider_hand, -math.degrees(self.angle))
        self.roteted_hit = pg.transform.rotate(self.collider_hit, -math.degrees(self.angle))

        scale = TILE_SIZE * self.game.IndexAlto

        # Mano
        center_x_world = (self.x + math.cos(self.angle) * self.hand_lado/32) * scale
        center_y_world = (self.y + math.sin(self.angle) * self.hand_lado/32) * scale
        self.rect_hand_world = self.roteted_hand.get_rect(center=(center_x_world, center_y_world))

        # Golpe
        center_x_world = (self.x + math.cos(self.angle) * self.hit_lado/32) * scale
        center_y_world = (self.y + math.sin(self.angle) * self.hit_lado/32) * scale
        self.rect_hit_world = self.roteted_hit.get_rect(center=(center_x_world, center_y_world))

    def draw(self):
        cam_x = self.game.camera_x
        cam_y = self.game.camera_y

        # Línea de dirección
        pg.draw.line(self.game.screen, 'yellow',
                     (self.x * TILE_SIZE * self.game.IndexAlto - cam_x,
                      self.y * TILE_SIZE * self.game.IndexAlto - cam_y),
                     (self.x * TILE_SIZE * self.game.IndexAlto - cam_x + ANCHO/4 * math.cos(self.angle),
                      self.y * TILE_SIZE * self.game.IndexAlto - cam_y + ANCHO/4 * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'yellow',
                       (self.x * TILE_SIZE * self.game.IndexAlto - cam_x,
                        self.y * TILE_SIZE * self.game.IndexAlto - cam_y), 5)
        pg.draw.circle(self.game.screen, (139, 69, 19),
                       (self.x * TILE_SIZE * self.game.IndexAlto - cam_x,
                        self.y * TILE_SIZE * self.game.IndexAlto - cam_y),
                       self.radius * TILE_SIZE * self.game.IndexAlto, 2)

        self.draw_hit()
        self.draw_hand()

    def update(self):
        self.movement()
        self.update_hitboxes()

    @property
    def pos(self):
        return (self.x, self.y)

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def draw_hand(self):
        if self.sttas['hand'] == 0 and self.hand_visible:
            cam_x = self.game.camera_x
            cam_y = self.game.camera_y
            # Dibujar la superficie rotada en la posición de pantalla
            rect_pantalla = self.roteted_hand.get_rect(
                center=(self.rect_hand_world.centerx - cam_x,
                        self.rect_hand_world.centery - cam_y)
            )
            self.game.screen.blit(self.roteted_hand, rect_pantalla)

    def create_hand(self):
        self.hand_lado = 15 * self.game.IndexAlto
        self.hand_color = (0, 0, 255)  # Azul
        self.time_hand = 0
        self.hand_ms = 300
        self.hand_visible = False
        self.collider_hand = pg.Surface((self.hand_lado, self.hand_lado), pg.SRCALPHA)
        # Dibujar el rectángulo en la superficie (borde azul)
        pg.draw.rect(self.collider_hand, self.hand_color, (0, 0, self.hand_lado, self.hand_lado), 2)
        self.roteted_hand = pg.transform.rotate(self.collider_hand, -math.degrees(self.angle))

    def draw_hit(self):
        if self.hit_visible:
            cam_x = self.game.camera_x
            cam_y = self.game.camera_y
            rect_pantalla = self.roteted_hit.get_rect(
                center=(self.rect_hit_world.centerx - cam_x,
                        self.rect_hit_world.centery - cam_y)
            )
            self.game.screen.blit(self.roteted_hit, rect_pantalla)

    def create_hit(self):
        self.hit_lado = 15 * self.game.IndexAlto
        self.hit_color = (255, 0, 0)  # Rojo
        self.time_hit = 0
        self.hit_ms = 300
        self.hit_visible = False
        self.collider_hit = pg.Surface((self.hit_lado, self.hit_lado), pg.SRCALPHA)
        pg.draw.rect(self.collider_hit, self.hit_color, (0, 0, self.hit_lado, self.hit_lado), 2)
        self.roteted_hit = pg.transform.rotate(self.collider_hit, -math.degrees(self.angle))
    
    def shoot(self):
        proj = Armas(self.game, self.x, self.y, self.angle)
        self.game.projectiles.add(proj)