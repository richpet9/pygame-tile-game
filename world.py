'''
World module handles creating a map, map operations, all that stuff
'''
import random
import pygame
import constants
from graphics import SpriteLoader
from objects import Tree
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

    def generate_forests(self, objects):
        '''
        Use cellular automata to generate some forests
        '''
        # Create random tree tiles
        for y in range(constants.MAP_HEIGHT):
            for x in range(constants.MAP_WIDTH):
                if(random.random() < 0.3 and self.tiles[x][y].terrain != "rock"):
                    self.tiles[x][y].contains_obj = Tree(x, y)
                    objects.append(self.tiles[x][y].contains_obj)

        # Using cellular automata
        # 5 passes are done
        for _ in range(5):
            for y in range(constants.MAP_HEIGHT):
                for x in range(constants.MAP_WIDTH):
                    current_tile = self.tiles[x][y]
                    neighbors = get_tile_neighbors(current_tile)
                    tree_neighbors = 0

                    for neighbor in neighbors:
                        if(has_tree(self.tiles[neighbor[0]][neighbor[1]])):
                            tree_neighbors += 1

                    if(not has_tree(current_tile) and tree_neighbors > 3 and current_tile.terrain != "rock"):
                        current_tile.contains_obj = Tree(x, y)
                        objects.append(self.tiles[x][y].contains_obj)
                    elif(has_tree(current_tile) and tree_neighbors < 2):
                        objects.remove(self.tiles[x][y].contains_obj)
                        current_tile.contains_obj = None

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
        self.location = (x, y)
        self.terrain = "snow" if random.random() < 0.85 else "rock"
        self.contains_obj = None
        self.transparent = True
        self.visible = True
        self.explored = False
        self.sprite = SpriteLoader.sprites.get(self.terrain)

    def get_rect(self):
        '''
        Return the rectangle pixel area of this tile
        '''
        return pygame.Rect(self.location[0] * constants.CELL_WIDTH,
                           self.location[1] * constants.CELL_HEIGHT,
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

    def center_at(self, location):
        '''
        Center the camera at the specified cell
        '''

        # Get centered coordinates
        centered_x = location[0] - (constants.CAMERA_WIDTH_CELL // 2)
        centered_y = location[1] - (constants.CAMERA_HEIGHT_CELL // 2)

        # Set the camera center cell
        self.set_cell((centered_x, centered_y))

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


def get_tile_neighbors(tile):
    '''
    Get all the neighboring coordinates for the specified tile
    '''
    if(not isinstance(tile, Tile)):
        raise TypeError("Invalid arguement for get_tile_neighbors: " +
                        " Got type '" +
                        type(tile).__name__ +
                        "' expected type '" +
                        Tile.__name__ + "'")

    res = []

    for y in range(3):
        for x in range(3):
            new_x = (tile.location[0] - 1) + x
            new_y = (tile.location[1] - 1) + y

            if(new_x < 0 or new_x > constants.MAP_WIDTH - 1):
                continue
            if(new_y < 0 or new_y > constants.MAP_HEIGHT - 1):
                continue
            if(new_x == tile.location[0] and new_y == tile.location[1]):
                continue

            res.append((new_x, new_y))

    return res


def has_tree(tile):
    if(tile.contains_obj):
        return tile.contains_obj.name == "tree"
    return False
