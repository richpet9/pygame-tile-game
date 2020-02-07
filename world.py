'''
World module handles creating a map, map operations, all that stuff
'''
import random
import pygame
import constants
from util import clamp

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
        width_cell = constants.DISPLAY_WIDTH // constants.CELL_WIDTH
        height_cell = constants.DISPLAY_HEIGHT // constants.CELL_HEIGHT

        for y_tile in range(camera.y_cell, camera.y_cell + height_cell):
            for x_tile in range(camera.x_cell, camera.x_cell + width_cell):
                if(x_tile < 0 or x_tile > constants.MAP_WIDTH - 1):
                    continue
                if(y_tile < 0 or y_tile > constants.MAP_HEIGHT - 1):
                    continue

                tile_to_draw = self.tiles[x_tile][y_tile]
                pygame.draw.rect(surface,
                                 TERRAIN_COLORS[tile_to_draw.terrain],
                                 pygame.Rect(x_tile * constants.CELL_WIDTH,
                                             y_tile * constants.CELL_HEIGHT,
                                             constants.CELL_WIDTH,
                                             constants.CELL_HEIGHT))


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
        return pygame.Rect(self.x_cell * constants.CELL_WIDTH,
                           self.y_cell * constants.CELL_WIDTH,
                           constants.CAMERA_WIDTH,
                           constants.CAMERA_HEIGHT)

    def set_cells(self, coords):
        self.x_cell = clamp(coords[0], 0,
                            constants.MAP_WIDTH - constants.CAMERA_WIDTH_CELL)
        self.y_cell = clamp(coords[1], 0,
                            constants.MAP_HEIGHT - constants.CAMERA_HEIGHT_CELL)
