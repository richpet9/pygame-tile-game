'''
The hud module contains the various HUD info screens and surfaces
'''
import pygame
from constants import DISPLAY_WIDTH, DISPLAY_HEIGHT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BORDER_WIDTH = 2
LINE_SPACING = 4


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
        _hud.__init__(self, DISPLAY_WIDTH // 5, DISPLAY_HEIGHT // 3)

        self.name = None
        self.health = None
        self.location = None

    def update_all_player_info(self, player):
        '''
        Update & Rerender all of the player info
        '''
        self.name = self.font.render(player.name, True, WHITE)
        self.health = self.font.render(
            'Health ' + str(player.health),
            True,
            WHITE)

        self.update_location(player.location)

    # DEBUG: In the future, we'll have separate methods to update each of the info items
    # I can probably put these all in a dictionary...
    def update_location(self, location):
        '''
        Update only location
        '''
        self.location = self.font.render(
            str(location[0]) + ' ' + str(location[1]),
            True,
            WHITE)

    def draw(self, surface_hud):
        '''
        Draw the hud to the specific surface
        '''
        self.surface.fill(BLACK)

        # Draw the border
        pygame.draw.rect(self.surface,
                         WHITE,
                         pygame.Rect(BORDER_WIDTH * 2,
                                     BORDER_WIDTH * 2,
                                     self.surface_width - (BORDER_WIDTH * 4),
                                     self.surface_height - (BORDER_WIDTH * 4)),
                         BORDER_WIDTH)

        self.surface.blit(self.name, (16, BORDER_WIDTH * 4))
        self.surface.blit(self.health, (16,
                                        self.font.get_linesize() +
                                        LINE_SPACING +
                                        (BORDER_WIDTH * 4)))
        self.surface.blit(self.location, (16,
                                          2 * self.font.get_linesize() +
                                          2 * LINE_SPACING +
                                          (BORDER_WIDTH * 4)))

        # Blit this hud's surface to the main hud surface
        surface_hud.blit(self.surface, (0, 0))
