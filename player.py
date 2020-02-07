from engine import GameObject


class Player(GameObject):
    def __init__(self, x, y):
        GameObject.__init__(self, x, y, (255, 200, 175))

    def move(self, direction):
        self.x_cell += direction[0]
        self.y_cell += direction[1]
