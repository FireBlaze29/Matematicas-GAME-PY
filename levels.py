import pygame as pg
from settings import TILE_SIZE

_ = False

Level1 = [[1, 1, 1, 1, 1, 1, 1, 1],
          [1, 0, 0, 0, 0, 0, 0, 1],
          [1, 0, 1, 1, 1, 1, 0, 1],
          [1, 0, 1, 0, 0, 1, 0, 1],
          [1, 0, 1, 0, 0, 1, 0, 1],
          [1, 1, 1, 1, 1, 1, 1, 1]]

class ChargeLevels:
    def __init__(self, game, level):
        self.game = game
        self.level = level
        self.world_map = {}
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.level):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value
    
    def draw(self):
        for pos in self.world_map:
            pg.draw.rect(self.game.screen, 'darkgray', (pos[0] * TILE_SIZE * self.game.IndexAlto, pos[1] * TILE_SIZE * self.game.IndexAlto, TILE_SIZE * self.game.IndexAlto, TILE_SIZE * self.game.IndexAlto), 2)