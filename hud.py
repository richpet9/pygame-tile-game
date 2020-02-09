'''
The hud module contains the various HUD info screens and surfaces
'''
import pygame
from constants import DISPLAY_WIDTH

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
        self.font_size = 16
        self.font = pygame.font.Font(
            "resources/8-BIT-WONDER.ttf", self.font_size, bold=False, italic=False)

    def draw_border(self):
        '''
        Draw a border around this HUD
        '''
        # Draw the border
        pygame.draw.rect(self.surface,
                         WHITE,
                         pygame.Rect(BORDER_WIDTH * 2,
                                     BORDER_WIDTH * 2,
                                     self.surface_width - (BORDER_WIDTH * 4),
                                     self.surface_height - (BORDER_WIDTH * 4)),
                         BORDER_WIDTH)


class hud_NearbyActions(_hud):
    '''
    The Nearby Actions menu which shows available movements on the right of the screen
    '''

    def __init__(self, width, height):
        super(hud_NearbyActions, self).__init__(width, height)

        self.action_list = []

    def add_action(self, action):
        '''
        Add action to action list HUD
        '''
        self.action_list.append(action)

    def draw(self, surface_hud):
        '''
        Draw the action list HUD
        '''

        # Clear the surface
        self.surface.fill(BLACK)

        # Draw a border
        self.draw_border()

        # Draw every action
        for key, action in enumerate(self.action_list):
            rendered_string = self.font.render(
                str(key) + ' ' + action["text"],
                False,
                WHITE)

            y_val = (key *
                     (self.font.get_linesize() + LINE_SPACING)) + (BORDER_WIDTH * 4)
            self.surface.blit(rendered_string, (BORDER_WIDTH * 6, y_val))

        # Blit this hud's surface to the main hud surface
        surface_hud.blit(self.surface,
                         ((DISPLAY_WIDTH * 4) // 5, (DISPLAY_WIDTH // 3)))


class hud_PlayerInfo(_hud):
    '''
    The player info hud element
    '''

    def __init__(self, width, height):
        super(hud_PlayerInfo, self).__init__(width, height)

        self.name = None
        self.health = None
        self.location = None

    def update_all_player_info(self, player):
        '''
        Update & Rerender all of the player info
        '''
        self.name = self.font.render(player.name, False, WHITE)
        self.health = self.font.render(
            'Health ' + str(player.health),
            False,
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
            False,
            WHITE)

    def draw(self, surface_hud):
        '''
        Draw the hud to the specific surface
        '''

        # Clear the hud surface
        self.surface.fill(BLACK)

        # Draw a border
        self.draw_border()

        # Blit the name
        self.surface.blit(self.name, (BORDER_WIDTH * 6, BORDER_WIDTH * 4))
        # Blit the health bar
        self.surface.blit(self.health, (BORDER_WIDTH * 6,
                                        self.font.get_linesize() +
                                        LINE_SPACING +
                                        (BORDER_WIDTH * 4)))
        # Blit the location info
        self.surface.blit(self.location, (BORDER_WIDTH * 6,
                                          2 * self.font.get_linesize() +
                                          2 * LINE_SPACING +
                                          (BORDER_WIDTH * 4)))

        # Blit this hud's surface to the main hud surface
        surface_hud.blit(self.surface, (0, 0))
