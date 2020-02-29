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
        x = self.location[0] + direction[0]
        y = self.location[1] + direction[1]
        self.location = (x, y)


def get_nearby_actions(player, tiles):
    '''
    Get the nearby actions for the specified player on the given tiles
    '''
    res = []
    for y in range(player.location[1] - 1, player.location[1] + 2):
        for x in range(player.location[0] - 1, player.location[0] + 2):
            neighbor_tile = tiles[x][y]
            if(neighbor_tile.contains_obj):
                for action in neighbor_tile.contains_obj.actions:
                    res.append(action)

    return res
