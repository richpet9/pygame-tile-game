'''
World module handles creating a map, map operations, all that stuff
'''
import random
import pygame
import constants
from graphics import SpriteLoader
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

        self.sprites = SpriteLoader.sprites

    def draw(self, surface, camera):
        '''
        Draw the map cells
        '''
        for y_tile in range(camera.y_cell, camera.y_cell + constants.CAMERA_HEIGHT_CELL):
            for x_tile in range(camera.x_cell, camera.x_cell + constants.CAMERA_WIDTH_CELL):
                self.tiles[x_tile][y_tile].draw(surface)


class Tile:
    '''
    Tiles occupy cells on the game board, make up the map
    '''

    def __init__(self, x, y):
        self.x_pos, self.y_pos = x, y
        self.terrain = "snow" if random.random() < 0.5 else "rock"
        self.contains_obj = None
        self.transparent = True
        self.visible = True
        self.explored = False
        self.sprite = SpriteLoader.sprites.get(self.terrain)

    def get_rect(self):
        '''
        Return the rectangle pixel area of this tile
        '''
        return pygame.Rect(self.x_pos * constants.CELL_WIDTH,
                           self.y_pos * constants.CELL_HEIGHT,
                           constants.CELL_WIDTH,
                           constants.CELL_HEIGHT)

    def check_transparency(self):
        '''
        Check if this tile is currently transparent or not
        '''
        if(self.contains_obj and self.contains_obj.transparent is False):
            return False

        return self.transparent

    def draw(self, surface):
        '''
        Draw this tile on the specified surface
        '''
        if(self.visible or self.explored):
            if(self.sprite and self.sprite.image[0]):
                # We have a sprite
                surface.blit(self.sprite.image[0], self.get_rect().topleft)
            else:
                # No sprite
                surface.fill((255, 0, 255), self.get_rect())

        # Check if this tile is not visible and explored
        if(not self.visible and self.explored):
            # Make darker
            overlay = pygame.Surface((self.get_rect().width,
                                      self.get_rect().height))
            overlay.fill((0, 0, 0, 205))
            surface.blit(overlay, self.get_rect().topleft)


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

    def set_cell(self, coords):
        '''
        Set the X cell and Y cell location of the camera's top left point
        '''
        self.x_cell = clamp(coords[0], 0,
                            constants.MAP_WIDTH - constants.CAMERA_WIDTH_CELL)
        self.y_cell = clamp(coords[1], 0,
                            constants.MAP_HEIGHT - constants.CAMERA_HEIGHT_CELL)
