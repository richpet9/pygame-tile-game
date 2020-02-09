'''
The Objects module contains all the game entities and the root object GameObject
'''

import pygame
import graphics
from constants import CELL_WIDTH, CELL_HEIGHT


class GameObject:
    '''
    Everything in the game that isn't a cell is a game object
    '''

    def __init__(self, x, y, color):
        self.x_cell = x
        self.y_cell = y
        self.x_pixel = x * CELL_WIDTH
        self.y_pixel = y * CELL_HEIGHT
        self.color = color
        self.sprite = None

    def get_rect(self):
        '''
        Return the pixel rectangle that this game object resides in
        '''

        return pygame.Rect(self.x_cell * CELL_WIDTH,
                           self.y_cell * CELL_HEIGHT,
                           CELL_WIDTH,
                           CELL_HEIGHT)

    def draw(self, surface, camera):
        '''
        Draw this GameObject on the specified surface
        '''

        # Check if camera has this object in view
        if(camera.get_rect().contains(self.get_rect())):
            if(self.sprite and self.sprite.image[0]):
                surface.blit(self.sprite.image[0],
                             (self.x_pixel, self.y_pixel))
            else:
                pygame.draw.rect(surface,
                                 self.color,
                                 self.get_rect())


class Tree(GameObject):
    '''A tree'''

    def __init__(self, x, y):
        super(Tree, self).__init__(x, y, color=(0, 255, 0))

        self.sprite = graphics.load_sprites().get('wood')
