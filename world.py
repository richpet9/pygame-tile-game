'''
World module handles creating a map, map operations, all that stuff
'''
import random
import pygame
from util import clamp
from constants import DISPLAY_WIDTH, DISPLAY_HEIGHT, CELL_WIDTH, CELL_HEIGHT, MAP_WIDTH, MAP_HEIGHT

TERRAIN_COLORS = {
    "snow": (200, 210, 225),
    "rock": (130, 140, 160)
}


class Map:
    '''
    The playable game map made up of tiles
    '''

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[Tile(x, y) for y in range(height)]
                      for x in range(width)]

    def draw(self, surface, camera):
        width_cell = DISPLAY_WIDTH // CELL_WIDTH
        height_cell = DISPLAY_HEIGHT // CELL_HEIGHT

        for y_tile in range(camera.y_cell, camera.y_cell + height_cell):
            for x_tile in range(camera.x_cell, camera.x_cell + width_cell):
                tile_to_draw = self.tiles[x_tile][y_tile]
                pygame.draw.rect(surface, TERRAIN_COLORS[tile_to_draw.terrain], pygame.Rect(
                    x_tile * CELL_WIDTH, y_tile * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))


class Tile:
    '''
    Tiles occupy cells on the game board, make up the map
    '''

    def __init__(self, x, y):
        self.x_pos, self.y_pos = x, y
        self.terrain = "snow" if random.random() < 0.5 else "rock"


class Camera:
    '''
    Controls what things are rendered
    '''

    def __init__(self, x, y):
        self.x_cell = x
        self.y_cell = y

    def get_rect(self):
        return pygame.Rect(self.x_cell * CELL_WIDTH,
                           self.y_cell * CELL_WIDTH,
                           DISPLAY_WIDTH,
                           DISPLAY_HEIGHT)

    def set_cells(self, coords):
        self.x_cell = clamp(coords[0], 0,
                            MAP_WIDTH - (DISPLAY_WIDTH // CELL_WIDTH))
        self.y_cell = clamp(coords[1], 0,
                            MAP_HEIGHT - (DISPLAY_HEIGHT // CELL_HEIGHT))
