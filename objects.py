'''
The Objects module contains all the game entities and the root object GameObject
'''

import pygame
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

        if(camera.get_rect().contains(self.get_rect())):
            pygame.draw.rect(surface, self.color, self.get_rect())


class Tree(GameObject):
    '''A tree'''

    def __init__(self, x, y):
        super(Tree, self).__init__(x, y, color=(0, 255, 0))
