'''
The hud module contains the various HUD info screens and surfaces
'''
import pygame
from constants import DISPLAY_WIDTH, DISPLAY_HEIGHT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class _hud:
    '''
    The inheireted HUD class which creates a surface for itself
    '''

    def __init__(self, width, height):
        self.surface = pygame.surface.Surface((width, height))
        self.surface_width = width
        self.surface_height = height
        self.font_size = 18
        self.font = pygame.font.Font(
            "resources/8-BIT-WONDER.ttf", self.font_size, bold=False, italic=False)


class hud_PlayerInfo(_hud):
    '''
    The player info hud element
    '''

    def __init__(self):
        _hud.__init__(self, DISPLAY_WIDTH // 5, DISPLAY_HEIGHT)

        self.name = None
        self.health = None
        self.location = None

    def update_all_player_info(self, player):
        '''
        Update & Rerender all of the player info
        '''
        self.name = self.font.render(player.name, True, WHITE)
        self.health = self.font.render(str(player.health) + '%', True, WHITE)
        self.location = self.font.render(str(player.location), True, WHITE)

    # DEBUG: In the future, we'll have separate methods to update each of the info items
    # I can probably put these all in a dictionary...
    def update_location(self, location):
        '''
        Update only location
        '''
        self.location = self.font.render(str(location), True, WHITE)

    def draw(self, surface_hud):
        '''
        Draw the hud to the specific surface
        '''
        self.surface.fill(BLACK)

        self.surface.blit(self.name, (16, 0))
        self.surface.blit(self.health, (16, self.font.get_linesize()))
        self.surface.blit(self.location, (16, 2 * self.font.get_linesize()))

        surface_hud.blit(self.surface, (0, 0))
