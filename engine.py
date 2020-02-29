'''
Engine handles initializing, starting, looping, and closing the game
'''
import sys
import pygame
import numpy as np
from tcod.map import compute_fov

import constants
import graphics
import world
import player
import hud
from util import clamp


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
        # Quit flag
        self.quit_game = False

        # Start pygame
        pygame.init()

        # Load Sprites
        graphics.SpriteLoader.load_sprites()

        # Create player variable
        self.player = None

        # Create game stats
        self.game_stats = GameStats()

        # Create Player Info hud
        self.player_info = hud.hud_PlayerInfoPanel(
            constants.DISPLAY_WIDTH // 5,
            constants.DISPLAY_HEIGHT // 3)

        # Nearby actions hud
        self.nearby_actions = hud.hud_NearbyActionsPanel(
            constants.DISPLAY_WIDTH // 5,
            (constants.DISPLAY_HEIGHT * 2) // 3)

        # Inspection panel hud
        self.inspection_panel = hud.hud_InspectionPanel(
            constants.DISPLAY_WIDTH // 5,
            constants.DISPLAY_HEIGHT // 3)

        # Cursor reference
        self.i_cursor = self.inspection_panel.cursor

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

    def handle_action_response(self, response):
        '''
        Handle an action response
        '''

        # Get the location
        location = response.get("location")
        tile = self.map.tiles[location[0]][location[1]]

        # Check response
        if(response.get("success")):
            # Check for destroy self flag
            if(response.get("destroy_self")):
                obj_to_destroy = tile.contains_obj
                tile.contains_obj = None
                self.objects.remove(obj_to_destroy)

            # Check for spawned objects flag
            for obj in response.get("spawned_objects"):
                self.objects.append(obj)
                self.map.tiles[obj.location[0]
                               ][obj.location[1]].contains_obj = obj

    def update_fov(self):
        '''
        Update the player's field of view
        '''
        # Create an array of transparency
        # TODO: Maybe have an array of transparency for the entire map
        #       stored in memory and updated when map changes?
        tiles = np.ones((constants.CAMERA_WIDTH_CELL + 1,
                         constants.CAMERA_HEIGHT_CELL + 1),
                        dtype=bool)
        # Get every visible tile
        for y_index, y_tile in enumerate(range(self.camera.location[1],
                                               self.camera.location[1] +
                                               constants.CAMERA_HEIGHT_CELL + 1)):
            for x_index, x_tile in enumerate(range(self.camera.location[0],
                                                   self.camera.location[0] +
                                                   constants.CAMERA_WIDTH_CELL + 1)):
                # Store it's visibility in 2d array
                tiles[x_index][y_index] = self.map.tiles[x_tile][y_tile].check_transparency()

        # Pass the array into tcod.map.compute_fov() with player's position
        res = compute_fov(
            tiles,
            (self.player.location[0] - self.camera.location[0],
             self.player.location[1] - self.camera.location[1]),
            radius=constants.FOV_RADIUS,
            algorithm=constants.FOV_ALG)

        # Go through the returned array and update every tile in that location
        for y_index, y_tile in enumerate(range(self.camera.location[1],
                                               self.camera.location[1] +
                                               constants.CAMERA_HEIGHT_CELL + 1)):
            for x_index, x_tile in enumerate(range(self.camera.location[0],
                                                   self.camera.location[0] +
                                                   constants.CAMERA_WIDTH_CELL + 1)):
                tile_to_update = self.map.tiles[x_tile][y_tile]
                tile_to_update.visible = res[x_index][y_index]
                tile_to_update.explored = True if res[x_index][y_index] else tile_to_update.explored

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

        # Update player info
        self.player_info.update_all_info(self.player, self.game_stats)

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
        # TODO: Create container for all the HUDs?
        self.player_info.draw(self.surface_hud)
        self.nearby_actions.draw(self.surface_hud, GameEngine.state)
        self.inspection_panel.draw(self.surface_hud)

        # Check if every object is visible, and draw the visible ones
        for game_object in self.objects:
            if(self.map.tiles[game_object.location[0]][game_object.location[1]].visible):
                game_object.draw(self.surface_map, self.camera)

        # Check if we are in inspect mode, and show the cursor if so
        if(GameEngine.state == "INSPECT" or GameEngine.state == "ACTIONS"):
            cell_location = (self.i_cursor.location[0] * constants.CELL_WIDTH,
                             self.i_cursor.location[1] * constants.CELL_HEIGHT)
            rect = pygame.Rect(cell_location[0],
                               cell_location[1],
                               constants.CELL_WIDTH,
                               constants.CELL_HEIGHT)
            self.surface_map.fill((255, 0, 255), rect)

        # Blit the surface map to the main surface
        self.surface_main.blit(self.surface_map,
                               ((constants.DISPLAY_WIDTH // 5),
                                0),
                               self.camera.get_rect())

        # Blit the surface hud to the main surface
        self.surface_main.blit(self.surface_hud, (0, 0))

    def handle_input(self, inputs):
        '''
        Handle all the inputs
        '''
        # Check inputs
        if(inputs.get("quit")):
            # Quit the game
            self.quit_game = True

        if(inputs.get("move_player")):
            # Get the direction
            direction = inputs.get("move_player")

            # Player move command
            if(GameEngine.state == "GAMEPLAY"):
                # Move the player
                self.player.move(direction)
                # Move inspection cursor with player
                self.i_cursor.move(direction)
                # Set the camera on the player
                self.camera.center_at(self.player.location)
                # Get new nearby actions
                self.nearby_actions.set_actions(player.get_nearby_actions(self.player,
                                                                          self.map.tiles))
                # Update FOV
                self.update_fov()
                # Increment turn
                self.increment_turn()
            elif(GameEngine.state == "ACTIONS"):
                # Change active action
                self.nearby_actions.move_active_action(direction)

                if(self.nearby_actions.has_actions()):
                    # Move the inspection cursor to the current action
                    self.i_cursor.set_location(
                        self.nearby_actions.get_active_action().location)
            elif(GameEngine.state == "INSPECT"):
                # Move the inspect cursor
                self.i_cursor.move(direction)

        if(inputs.get("toggle_actions")):
            # Toggle the action select mode
            if(GameEngine.state != "ACTIONS"):
                GameEngine.state = "ACTIONS"
                if(self.nearby_actions.has_actions()):
                    # Move the inspection cursor to the current action
                    self.i_cursor.set_location(
                        self.nearby_actions.get_active_action().location)
            else:
                # Toggle off action menu
                GameEngine.state = "GAMEPLAY"
                # Reset the cursor to players location
                self.i_cursor.set_location(self.player.location)

        if(inputs.get("toggle_inspect")):
            # Toggle the inspect mode
            if(GameEngine.state != "INSPECT"):
                # Set inspection mode if not in it
                GameEngine.state = "INSPECT"
            else:
                # Set to gameplay if in inspection mode
                GameEngine.state = "GAMEPLAY"
                # Reset the cursor to players location
                self.i_cursor.set_location(self.player.location)

        if(inputs.get("return")):
            if(GameEngine.state == "ACTIONS"):
                if(self.nearby_actions.has_actions()):
                    # Get the action
                    active_action = self.nearby_actions.get_active_action()

                    # Commit the action
                    self.handle_action_response(active_action.act())

                    # Update FOV
                    self.update_fov()
                    self.increment_turn()

                    # Get new nearby actions
                    self.nearby_actions.set_actions(
                        player.get_nearby_actions(self.player, self.map.tiles))

                    # If we have new actions, be sure to move the inspection cursor to it
                    if(self.nearby_actions.has_actions()):
                        # Move the inspection cursor to the current action
                        self.i_cursor.set_location(
                            self.nearby_actions.get_active_action().location)
                    else:
                        # If we don't have more actions, leave action mode
                        GameEngine.state = "GAMEPLAY"
                        # Reset the cursor to players location
                        self.i_cursor.set_location(
                            self.player.location)

        # We do this stuff after EVERY input
        # Update player location in the hud
        self.player_info.update_location(self.player.location)

        # Update inspection panel info
        self.inspection_panel.inpsected_tile = self.map.tiles[
            self.i_cursor.location[0]][
            self.i_cursor.location[1]]

    def start(self):
        '''
        Begins the game loop
        '''

        # Create a player
        self.player = player.Player(constants.CAMERA_WIDTH_CELL // 2,
                                    constants.CAMERA_HEIGHT_CELL // 2)
        # Add player to objects list
        self.objects.append(self.player)

        # TEmp map generation
        self.map.generate_forests(self.objects)

        # First time update of player HUD and inspection cursor location
        self.player_info.update_all_info(self.player, self.game_stats)
        self.i_cursor.set_location(self.player.location)

        # First time fov compute
        self.update_fov()

        # Start the main loop of the game
        self.main_loop()

    def main_loop(self):
        '''
        The main game loop while running
        '''

        # When this is True we will quit
        self.quit_game = False

        # While we don't want to quit the game
        while not self.quit_game:
            # Get inputs
            inputs = get_inputs()

            # Handle inputs
            self.handle_input(inputs)

            # Draw everything
            self.draw()

            # Update the display
            pygame.display.update()

            # Limit Framerate to 15 fps
            self.clock.tick(15)

        # Exit the application
        pygame.quit()
        sys.exit()


def get_inputs():
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
            if(event.key == pygame.K_i):
                res["toggle_inspect"] = True

    return res


if __name__ == '__main__':
    ge = GameEngine()
    ge.start()
