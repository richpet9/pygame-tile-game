'''
Engine handles initializing, starting, looping, and closing the game
'''
import sys
import pygame
import constants
import world
import player
import hud
import objects


class GameEngine:
    '''
    The driving force of the program, holds the main game loop
    '''

    def __init__(self):
        '''
        Loads all the game modules required
        '''

        # Start pygame
        pygame.init()

        # Create player variable
        self.player = None

        # Create Player Info hud
        self.player_info = hud.hud_PlayerInfo(
            constants.DISPLAY_WIDTH // 5,
            constants.DISPLAY_HEIGHT // 3)

        # Near by actions hud
        self.nearby_actions = hud.hud_NearbyActions(
            constants.DISPLAY_WIDTH // 5,
            (constants.DISPLAY_HEIGHT * 2) // 3)

        # Create the camera
        self.camera = world.Camera(0, 0)

        # Create the main game surface
        self.surface_main = pygame.display.set_mode((constants.DISPLAY_WIDTH,
                                                     constants.DISPLAY_HEIGHT))
        # Create the map surface
        self.surface_map = pygame.Surface((constants.MAP_WIDTH * constants.CELL_WIDTH,
                                           constants.MAP_HEIGHT * constants.CELL_HEIGHT))
        # Create the hud surface
        self.surface_hud = pygame.Surface((constants.DISPLAY_WIDTH,
                                           constants.DISPLAY_HEIGHT))
        # Create the pygame clock
        self.clock = pygame.time.Clock()

        # Create the map
        self.map = world.Map(constants.MAP_WIDTH, constants.MAP_HEIGHT)

        # Create the object container
        self.objects = []

    def start(self):
        '''
        Begins the game loop
        '''

        # Create a player
        self.player = player.Player(constants.CAMERA_WIDTH_CELL // 2,
                                    constants.CAMERA_HEIGHT_CELL // 2)
        # Add player to objects list
        self.objects.append(self.player)

        # Create some trees for debuggin
        for i in range(10):
            new_tree = objects.Tree(i + 10, i + 10)
            self.objects.append(new_tree)

        # Update HUD
        self.player_info.update_all_player_info(self.player)

        self.nearby_actions.add_action({"text": "Example Action"})
        self.nearby_actions.add_action({"text": "Example Action"})
        self.nearby_actions.add_action({"text": "Example Action"})

        # DEBUG: Set the camera to (0, 0) (temporary)
        self.camera.set_cells((0, 0))

        # Start the main loop of the game
        self.main_loop()

    def main_loop(self):
        '''
        The main game loop while running
        '''

        # When this is True we will quit
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
                self.camera.set_cells((self.player.x_cell - (constants.CAMERA_WIDTH_CELL // 2),
                                       self.player.y_cell - (constants.CAMERA_HEIGHT_CELL // 2)))

            # Update player info hud
            self.player_info.update_location(self.player.location)

            # Draw everything
            self.draw()

            # Update the display
            pygame.display.update()

            # Limit Framerate to 15 fps
            self.clock.tick(15)

        # Exit the application
        pygame.quit()
        sys.exit()

    def draw(self):
        '''
        Draw all the things in the game
        '''

        # Clear both surfaces with black
        self.surface_main.fill(pygame.Color(0, 0, 0))
        self.surface_map.fill(pygame.Color(0, 0, 0))
        self.surface_hud.fill(pygame.Color(0, 0, 0, 0))

        # Draw the map onto the surface map
        self.map.draw(self.surface_map, self.camera)

        # Draw the player info
        self.player_info.draw(self.surface_hud)
        self.nearby_actions.draw(self.surface_hud)

        # Check if every object is visible, and draw the visible ones
        for game_object in self.objects:
            game_object.draw(self.surface_map, self.camera)

        # Blit the surface map to the main surface
        self.surface_main.blit(self.surface_map,
                               (constants.DISPLAY_WIDTH // 5,
                                constants.CELL_HEIGHT // 2),
                               self.camera.get_rect())

        # Blit the surface hud to the main surface
        self.surface_main.blit(self.surface_hud, (0, 0))


def handle_input():
    '''
    Handle input events
    '''

    # Get the list of inputs
    events_list = pygame.event.get()
    # Return dictionary
    res = {}

    # For every event
    for event in events_list:
        # If quit is requested, add quit to dictionary
        if(event.type == pygame.QUIT):
            res['quit'] = True

        # If a key was pressed
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
