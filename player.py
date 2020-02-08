'''
Module for handling player operations and info
'''

from objects import GameObject


class Player(GameObject):
    '''
    A player in the game, controlled by a user
    '''

    def __init__(self, x, y):
        super(Player, self).__init__(x, y, (255, 200, 175))

        self.name = "Richie"
        self.health = 100
        self.location = (x, y)

    def move(self, direction):
        '''
        Move the player is the specified direction
        direction: Tuple (int, int) the (x, y) distance to move
        '''
        self.x_cell += direction[0]
        self.y_cell += direction[1]
        self.location = (self.x_cell, self.y_cell)
