'''
Engine handles initializing, starting, looping, and closing the game
'''
import sys
import pygame
import constants
import graphics
import world
import player
import hud
import objects
import tcod as libtcodpy
import numpy as np


class GameStats:
    '''
    GameStats stores all the current stats for the game / life
    '''

    def __init__(self):
        self.turn_count = 0
        self.time = (12, 00)
        self.date = (8, "January")


class GameEngine:
    '''
    The driving force of the program, holds the main game loop
    '''
    state = "GAMEPLAY"

    def __init__(self):
        '''
        Loads all the game modules required
        '''

        # Start pygame
        pygame.init()

        # Load Sprites
        graphics.SpriteLoader.load_sprites()

        # Create player variable
        self.player = None

        # Create game stats
        self.game_stats = GameStats()

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

        # Active action reference
        self.active_action = None

    def update_fov(self):
        '''
        Update the player's field of view
        '''
        # Create an array of transparency
        # TODO: Maybe have an array of transparency for the entire map
        # stored in memory and updated when map changes?
        tiles = np.ones((constants.CAMERA_WIDTH_CELL,
                         constants.CAMERA_HEIGHT_CELL), dtype=bool)
        # Get every visible tile
        for y_index, y_tile in enumerate(range(self.camera.y_cell, self.camera.y_cell + constants.CAMERA_HEIGHT_CELL)):
            for x_index, x_tile in enumerate(range(self.camera.x_cell, self.camera.x_cell + constants.CAMERA_WIDTH_CELL)):
                # Store it's visibility in 2d array
                tiles[x_index][y_index] = self.map.tiles[x_tile][y_tile].check_transparency()

        # Pass the array into tcod.map.compute_fov() with player's position
        res = libtcodpy.map.compute_fov(
            tiles,
            (self.player.x_cell - self.camera.x_cell,
             self.player.y_cell - self.camera.y_cell),
            constants.CAMERA_WIDTH_CELL,
            algorithm=libtcodpy.FOV_PERMISSIVE_5)

        # Go through the returned array and update every tile in that location
        for y_index, y_tile in enumerate(range(self.camera.y_cell, self.camera.y_cell + constants.CAMERA_HEIGHT_CELL)):
            for x_index, x_tile in enumerate(range(self.camera.x_cell, self.camera.x_cell + constants.CAMERA_WIDTH_CELL)):
                self.map.tiles[x_tile][y_tile].visible = res[x_index][y_index]

    def increment_turn(self):
        '''
        Increment one game turn
        '''
        self.game_stats.turn_count += 1
        new_time = (
            self.game_stats.time[0],    # Hours
            self.game_stats.time[1] + constants.MINUTES_PER_TURN    # Minutes
        )

        # Adjust for time overflow
        if(new_time[1] > 59):
            new_time = (new_time[0] + 1, 0)
        if(new_time[0] > 23):
            new_time = (0, new_time[1])
        self.game_stats.time = new_time

        self.player_info.update_all_info(self.player, self.game_stats)

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
            self.map.tiles[i + 10][i + 10].contains_obj = new_tree
            self.objects.append(new_tree)

        # DEBUG: Set the camera to (0, 0) (temporary)
        self.camera.set_cell((0, 0))

        # First time update of player HUD
        self.player_info.update_all_info(
            self.player, self.game_stats)

        # First time fov compute
        self.update_fov()

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
            if(inputs.get("quit")):
                # Quit the game
                quit_game = True
            if(inputs.get("move_player")):
                direction = inputs.get("move_player")
                # Player move command
                if(GameEngine.state == "GAMEPLAY"):
                    # Move the player
                    self.player.move(direction)
                    # Set the camera on the player
                    centered_x = self.player.x_cell - \
                        (constants.CAMERA_WIDTH_CELL // 2)
                    centered_y = self.player.y_cell - \
                        (constants.CAMERA_HEIGHT_CELL // 2)
                    # Set the camera center cell
                    self.camera.set_cell((centered_x, centered_y))
                    # Get new nearby actions
                    self.nearby_actions.set_actions(player.get_nearby_actions(self.player,
                                                                              self.map.tiles))
                    # Update FOV
                    self.update_fov()
                    # Update HUD
                    self.increment_turn()
                else:
                    # Change active action
                    self.nearby_actions.move_active_action(
                        direction)
            if(inputs.get("toggle_actions")):
                # Toggle the action select mode
                GameEngine.state = "ACTIONS" if GameEngine.state != "ACTIONS" else "GAMEPLAY"
            if(inputs.get("return")):
                if(GameEngine.state == "ACTIONS"):
                    if(self.nearby_actions.has_actions()):
                        # Get the action
                        active_action = self.nearby_actions.action_list[self.nearby_actions.active_action]

                        # Commit the action
                        action_response = active_action.act()

                        # Check response
                        if(action_response.get("success")):
                            if(action_response.get('destroy_self')):
                                tile = self.map.tiles[active_action.cell[0]
                                                      ][active_action.cell[1]]
                                obj_to_destroy = tile.contains_obj
                                tile.contains_obj = None
                                self.objects.remove(obj_to_destroy)
                            if(action_response.get('spawned_objects') is not None):
                                self.objects.append(
                                    action_response.get('spawned_objects')[0])
                            # Update FOV
                            self.update_fov()
                            self.increment_turn()

                            # Get new nearby actions
                            self.nearby_actions.set_actions(
                                player.get_nearby_actions(self.player, self.map.tiles))

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
        self.nearby_actions.draw(self.surface_hud, GameEngine.state)

        # Check if every object is visible, and draw the visible ones
        for game_object in self.objects:
            if(self.map.tiles[game_object.x_cell][game_object.y_cell].visible):
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
            res["quit"] = True

        # If a key was pressed
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_ESCAPE):
                res["quit"] = True
            if(event.key == pygame.K_w):
                res["move_player"] = (0, -1)
            if(event.key == pygame.K_a):
                res["move_player"] = (-1, 0)
            if(event.key == pygame.K_s):
                res["move_player"] = (0, 1)
            if(event.key == pygame.K_d):
                res["move_player"] = (1, 0)
            if(event.key == pygame.K_e):
                res["toggle_actions"] = True
            if(event.key == pygame.K_RETURN):
                res["return"] = True

    return res


if __name__ == '__main__':
    ge = GameEngine()
    ge.start()
