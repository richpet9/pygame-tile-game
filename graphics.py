'''
This module contains various classes and functions for graphics manipulation
'''

import pygame
from constants import CELL_WIDTH, CELL_HEIGHT, DISPLAY_WIDTH


class Sprite:
    '''
    A pygame surface containing a scaled image to represent objects
    '''

    def __init__(self, file_path, animates=False):
        self.animates = animates

        if(not animates):
            self.image = [pygame.transform.scale(
                pygame.image.load(file_path), (CELL_WIDTH, CELL_HEIGHT)
            )]
        else:
            # Load in multiple images from sprite sheet
            return


class SpriteLoader:
    '''
    Sprite Loader handles keeping all our image references in one place
    '''
    sprites = {}

    @staticmethod
    def load_sprites():
        '''
        This static method can be called with .get() to get any image references
        '''
        SpriteLoader.sprites = {
            "snow": Sprite("resources/sprites/snow.png"),
            "rock": Sprite("resources/sprites/rock.png"),
            "tree": Sprite("resources/sprites/tree.png"),
            "wood": Sprite("resources/sprites/wood.png"),
            "cursor": Sprite("resources/sprites/cursor.png")
        }


class Renderer:
    '''
    Renders the game
    '''

    def __init__(self, surface_main, surface_map, surface_hud, camera):
        self.surface_main = surface_main
        self.surface_map = surface_map
        self.surface_hud = surface_hud
        self.camera = camera

    def render_all(self, gamestate, game_map, object_container, hud_container):
        '''
        Render the entire game
        '''

        # Clear all surfaces with black
        self.surface_main.fill(pygame.Color(0, 0, 0))
        self.surface_map.fill(pygame.Color(0, 0, 0))
        self.surface_hud.fill(pygame.Color(0, 0, 0, 0))

        # Draw the map onto the surface map
        game_map.draw(self.surface_map, self.camera)

        # Draw the HUDs
        hud_container.draw_each(self.surface_hud)

        # Check if every object is visible, and draw the visible ones
        for game_object in object_container:
            if(game_map.tiles[game_object.location[0]][game_object.location[1]].visible):
                game_object.draw(self.surface_map, self.camera)

        # Check if we are in inspect mode, and show the cursor if so
        if(gamestate in ("INSPECT", "ACTIONS")):
            cursor = hud_container.get_hud("INSPECTION_PANEL").cursor

            cell_location = (cursor.location[0] * CELL_WIDTH,
                             cursor.location[1] * CELL_HEIGHT)

            self.surface_map.blit(SpriteLoader.sprites.get("cursor").image[0],
                                  (cell_location[0], cell_location[1]))

        # Blit the surface map to the main surface
        self.surface_main.blit(self.surface_map,
                               ((DISPLAY_WIDTH // 5),
                                0),
                               self.camera.get_rect())

        # Blit the surface hud to the main surface
        self.surface_main.blit(self.surface_hud, (0, 0))
