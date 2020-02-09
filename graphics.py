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


# TODO: This can be optimzed
def load_sprites():
    '''
    Returns a dictionary of loaded sprites
    '''

    return {
        "snow": Sprite("resources/sprites/snow.png"),
        "rock": Sprite("resources/sprites/rock.png"),
        "wood": Sprite("resources/sprites/wood.png")
    }
