'''
World module handles creating a map, map operations, all that stuff
'''
import random
import pygame
import constants
import graphics
import objects
from util import clamp

TERRAIN_COLORS = {
    "snow": (200, 210, 225),
    "rock": (130, 140, 160)
}

CURRENT_MAP = None


class Map:
    '''
    The playable game map made up of tiles
    '''

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = [[Tile(x, y) for y in range(height)]
                      for x in range(width)]

        self.sprites = graphics.load_sprites()

    def place_tree(self, x, y):
        self.tiles[x][y].contains_obj.append(objects.Tree(x, y))

    def draw(self, surface, camera):
        '''
        Draw the map cells
        '''
        for y_tile in range(camera.y_cell, camera.y_cell + constants.CAMERA_HEIGHT_CELL):
            for x_tile in range(camera.x_cell, camera.x_cell + constants.CAMERA_WIDTH_CELL):
                tile_to_draw = self.tiles[x_tile][y_tile]
                sprite = self.sprites.get(tile_to_draw.terrain)

                if(sprite and sprite.image[0]):
                    surface.blit(sprite.image[0], (x_tile * constants.CELL_WIDTH,
                                                   y_tile * constants.CELL_HEIGHT))
                else:
                    pygame.draw.rect(surface,
                                     (255, 0, 255),
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
        self.contains_obj = []


class Camera:
    '''
    Controls what things are rendered
    '''

    def __init__(self, x, y):
        self.x_cell = x
        self.y_cell = y

    def get_rect(self):
        '''
        Return the pixel rectangle that this object can see
        '''
        return pygame.Rect((self.x_cell * constants.CELL_WIDTH),
                           (self.y_cell * constants.CELL_WIDTH),
                           constants.CAMERA_WIDTH - constants.CELL_WIDTH,
                           constants.CAMERA_HEIGHT - constants.CELL_HEIGHT)

    def set_cells(self, coords):
        '''
        Set the X cell and Y cell location of the camera's top left point
        '''
        self.x_cell = clamp(coords[0], 0,
                            constants.MAP_WIDTH - constants.CAMERA_WIDTH_CELL)
        self.y_cell = clamp(coords[1], 0,
                            constants.MAP_HEIGHT - constants.CAMERA_HEIGHT_CELL)
