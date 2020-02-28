'''
Module for handling player operations and info
'''

from objects import GameObject


class Player(GameObject):
    '''
    A player in the game, controlled by a user
    '''

    def __init__(self, x, y):
        super(Player, self).__init__(x, y, (255, 200, 175), name="Richie")

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


def get_nearby_actions(player, tiles):
    '''
    Get the nearby actions for the specified player on the given tiles
    '''
    res = []
    for _y in range(player.y_cell - 1, player.y_cell + 2):
        for _x in range(player.x_cell - 1, player.x_cell + 2):
            neighbor_tile = tiles[_x][_y]
            if(neighbor_tile.contains_obj):
                for action in neighbor_tile.contains_obj.actions:
                    res.append(action)

    return res
