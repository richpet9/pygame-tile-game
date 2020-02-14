'''
This module contains various classes and functions for graphics manipulation
'''

import pygame
from constants import CELL_WIDTH, CELL_HEIGHT


class Sprite:
    '''
    A pygame surface containing a scaled image to represent objects
    '''

    def __init__(self, file_path, animates=False):
        self.animates = animates

        if(not animates):
            self.image = [pygame.transform.scale(
                pygame.image.load(file_path), (CELL_WIDTH, CELL_HEIGHT))]
        else:
            # Load in multiple images from sprite sheet
            return


class SpriteLoader:
    '''
    Sprite Loader handles keeping all our image references in one place
    '''
    sprites = {}

    @staticmethod
    def load_sprites():
        '''
        This static method can be called with .get() to get any image references
        '''
        SpriteLoader.sprites = {
            "snow": Sprite("resources/sprites/snow.png"),
            "rock": Sprite("resources/sprites/rock.png"),
            "tree": Sprite("resources/sprites/tree.png"),
            "wood": Sprite("resources/sprites/wood.png")
        }
