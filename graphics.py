'''
This module contains various classes and functions for graphics manipulation
'''

import pygame


class Sprite:
    def __init__(self, file_path, animates=False):
        self.animates = animates

        if(not animates):
            self.image = [pygame.image.load(file_path)]
        else:
            # Load in multiple images from sprite sheet
            return


def load_sprites():
    return {
        "snow": Sprite("resources/sprites/snow.png"),
        "rock": Sprite("resources/sprites/rock.png")
    }
