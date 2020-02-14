'''
The hud module contains the various HUD info screens and surfaces
'''
import pygame
from constants import DISPLAY_WIDTH

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (250, 0, 0)
GRAY = (150, 150, 150)

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

    def draw_border(self, active=False):
        '''
        Draw a border around this HUD
        '''

        # Conditional color
        color = WHITE if not active else RED
        # Draw the border
        pygame.draw.rect(self.surface,
                         color,
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
        self.active_action = -1
        self.header = self.font.render("Nearby Actions", False, WHITE)

    def move_active_action(self, direction):
        '''
        Move the active selected action by the specified tuple distance
        '''
        if(self.has_actions()):
            self.active_action = (self.active_action +
                                  direction[1]) % len(self.action_list)
        else:
            self.active_action = -1

    def has_actions(self):
        '''
        If there are actions in the list
        '''
        return len(self.action_list) > 0

    def set_actions(self, actions):
        '''
        Set the action lists
        '''

        # Check if the list of actions is empty or not
        if(len(actions) > 0):
            self.action_list = actions
        else:
            # If it's empty, be sure to reset active_action to 0
            self.action_list = []
            self.active_action = 0

    def draw(self, surface_hud, gamestate):
        '''
        Draw the action list HUD
        '''

        # Clear the surface
        self.surface.fill(BLACK)

        # Draw a border
        if(gamestate == "ACTIONS"):
            self.draw_border(active=True)
        else:
            self.draw_border()

        # Draw header for HUD
        self.surface.blit(self.header, (
            BORDER_WIDTH * 6,
            BORDER_WIDTH * 4
        ))

        # Draw every action
        for key, action in enumerate(self.action_list):
            color = GRAY
            # Check if the current active action if the action we are rendering
            if(self.active_action == key and gamestate == "ACTIONS"):
                color = RED

            # TODO: Cache this render
            rendered_string = self.font.render(str(key) + ' ' + action.text,
                                               False,
                                               color)

            x_val = BORDER_WIDTH * 6
            y_val = ((key + 1) * (self.font.get_linesize() +
                                  LINE_SPACING)) + (BORDER_WIDTH * 4)

            self.surface.blit(rendered_string, (x_val, y_val))

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
