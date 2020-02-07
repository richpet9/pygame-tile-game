'''
Engine handles initializing, starting, looping, and closing the game
'''
import sys
import pygame
import constants
import world
import player

constants.DISPLAY_WIDTH_CELL = constants.DISPLAY_WIDTH // constants.CELL_WIDTH
constants.DISPLAY_HEIGHT_CELL = constants.DISPLAY_HEIGHT // constants.CELL_HEIGHT


class GameObject:
    '''
    Everything in the game that isn't a cell is a game object
    '''

    def __init__(self, x, y, color):
        self.x_cell = x
        self.y_cell = y
        self.x_pixel = x * constants.CELL_WIDTH
        self.y_pixel = y * constants.CELL_HEIGHT
        self.color = color

    def get_rect(self):
        return pygame.Rect(self.x_cell * constants.CELL_WIDTH,
                           self.y_cell * constants.CELL_HEIGHT,
                           constants.CELL_WIDTH,
                           constants.CELL_HEIGHT)

    def draw(self, surface, camera):
        if(camera.get_rect().contains(self.get_rect())):
            pygame.draw.rect(surface, self.color, self.get_rect())


class GameEngine:
    '''
    The driving force of the program, holds the main game loop
    '''

    def __init__(self):
        '''
        Loads all the game modules required
        '''

        pygame.init()

        self.player = None

        self.surface_main = pygame.display.set_mode((constants.DISPLAY_WIDTH,
                                                     constants.DISPLAY_HEIGHT))
        self.surface_map = pygame.Surface((constants.MAP_WIDTH * constants.CELL_WIDTH,
                                           constants.MAP_HEIGHT * constants.CELL_HEIGHT))
        self.clock = pygame.time.Clock()
        self.camera = world.Camera(0, 0)
        self.map = world.Map(constants.MAP_WIDTH, constants.MAP_HEIGHT)

        self.objects = []

    def start(self):
        '''
        Begins the game loop
        '''
        self.player = player.Player(constants.DISPLAY_WIDTH_CELL // 2,
                                    constants.DISPLAY_HEIGHT_CELL // 2)
        self.objects.append(self.player)

        self.camera.set_cells((self.player.x_cell - (constants.DISPLAY_WIDTH_CELL // 2),
                               self.player.y_cell - (constants.DISPLAY_HEIGHT_CELL // 2)))

        self.main_loop()

    def main_loop(self):
        '''
        The main game loop while running
        '''

        quit_game = False

        # While we don't want to quit the game
        while not quit_game:
            # Get inputs
            inputs = handle_input()

            # Check inputs
            if(inputs.get('quit')):
                quit_game = True
            if(inputs.get('move_player')):
                self.player.move(inputs.get('move_player'))
                self.camera.set_cells((self.player.x_cell - (constants.DISPLAY_WIDTH_CELL // 2),
                                       self.player.y_cell - (constants.DISPLAY_HEIGHT_CELL // 2)))

            # Draw everything
            self.draw()

            # Update the display
            pygame.display.update()

            # Limit Framerate to 15 fps
            self.clock.tick(15)

        pygame.quit()
        sys.exit()

    def draw(self):
        '''
        Draw all the things in the game
        '''

        # Clear both surfaces with black
        self.surface_main.fill(pygame.Color(0, 0, 0))
        self.surface_map.fill(pygame.Color(0, 0, 0))

        # Draw the map onto the surface map
        self.map.draw(self.surface_map, self.camera)

        # Check if every object is visible, and draw the visible ones
        for game_object in self.objects:
            game_object.draw(self.surface_map, self.camera)

        # Blit the surface map to the main surface
        self.surface_main.blit(self.surface_map, (0, 0),
                               self.camera.get_rect())


def handle_input():
    '''
    Handle input events
    '''

    events_list = pygame.event.get()

    res = {}

    for event in events_list:
        if(event.type == pygame.QUIT):
            res['quit'] = True

        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_ESCAPE):
                res['quit'] = True
            if(event.key == pygame.K_w):
                res['move_player'] = (0, -1)
            if(event.key == pygame.K_a):
                res['move_player'] = (-1, 0)
            if(event.key == pygame.K_s):
                res['move_player'] = (0, 1)
            if(event.key == pygame.K_d):
                res['move_player'] = (1, 0)

    return res


if __name__ == '__main__':
    ge = GameEngine()
    ge.start()
