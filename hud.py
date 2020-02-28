'''
The hud module contains the various HUD info screens and surfaces
'''
import pygame
from util import format_time
from constants import DISPLAY_WIDTH, DISPLAY_HEIGHT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (250, 0, 0)
GRAY = (150, 150, 150)

BORDER_WIDTH = 1
LINE_SPACING = 4


class _hud:
    '''
    The inheireted HUD class which creates a surface for itself
    '''

    def __init__(self, width, height):
        self.surface = pygame.surface.Surface((width, height))
        self.surface_width = width
        self.surface_height = height
        self.font_size = 32
        self.font = pygame.font.Font(
            "resources/Deltoid-sans.ttf", self.font_size, bold=False, italic=False)

    def draw_border(self, color=None):
        '''
        Draw a border around this HUD
        '''

        # Conditional color
        color = WHITE if not color else color
        # Draw the border
        pygame.draw.rect(self.surface,
                         color,
                         pygame.Rect(BORDER_WIDTH * 2,
                                     BORDER_WIDTH * 2,
                                     self.surface_width - (BORDER_WIDTH * 4),
                                     self.surface_height - (BORDER_WIDTH * 4)),
                         BORDER_WIDTH)


class hud_InspectionPanel(_hud):
    '''
    The "inspect" area of the hud which shows what the player is "looking at"
    Controls a cursor that moves around the map when in inspect mode
    '''

    def __init__(self, width, height):
        super(hud_InspectionPanel, self).__init__(width, height)

        # The currently inspected tile
        self.inpsected_tile = None

    def draw(self, surface_hud):
        '''
        Draw the inspection panel
        '''

        # Clear the surface
        self.surface.fill(BLACK)

        # Draw a border
        self.draw_border()

        # Draw the current tile info
        if(self.inpsected_tile):
            # Render terrain string
            tile_terrain = self.font.render(
                "Terrain: " + self.inpsected_tile.terrain, True, WHITE)
            # Blit terrain string
            self.surface.blit(tile_terrain, (BORDER_WIDTH + 10, BORDER_WIDTH))

            # Check if there is an object on this tile
            if(self.inpsected_tile.contains_obj):
                # Render object string
                tile_object = self.font.render(
                    "Object: " + self.inpsected_tile.contains_obj, True, WHITE)
                # Blit object string
                self.surface.blit(
                    tile_object, (BORDER_WIDTH + 10, BORDER_WIDTH))

        surface_hud.blit(self.surface,
                         ((DISPLAY_WIDTH * 4) // 5, 0))


class hud_NearbyActionsPanel(_hud):
    '''
    The Nearby Actions menu which shows available movements on the right of the screen
    '''

    def __init__(self, width, height):
        super(hud_NearbyActionsPanel, self).__init__(width, height)

        self.action_list = []
        self.active_action = -1
        self.header = self.font.render("Nearby Actions", False, WHITE)

    def get_active_action(self):
        '''
        Get the active action from the current index
        '''
        return self.action_list[self.active_action]

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
            self.draw_border(color=RED)
        else:
            self.draw_border()

        # Draw header for HUD
        self.surface.blit(self.header, (
            BORDER_WIDTH + 10,
            BORDER_WIDTH
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
                         ((DISPLAY_WIDTH * 4) // 5, (DISPLAY_HEIGHT // 3)))


class hud_PlayerInfoPanel(_hud):
    '''
    The player info hud element
    '''

    def __init__(self, width, height):
        super(hud_PlayerInfoPanel, self).__init__(width, height)

        self.name = None
        self.health = None
        self.location = None
        self.time = None
        self.date = None
        self.turn_count = None

    def update_all_info(self, player, game_stats):
        '''
        Update & Rerender all of the player info
        '''
        self.update_name(player.name)
        self.update_health(player.health)
        self.update_location(player.location)
        self.update_time(game_stats.time)
        self.update_date(game_stats.date)
        self.update_turn_count(game_stats.turn_count)

    def update_name(self, name):
        '''
        Update only name
        '''
        self.name = self.font.render(
            str(name),
            False,
            WHITE)

    def update_health(self, health):
        '''
        Update only health
        '''
        self.health = self.font.render(
            str(health),
            False,
            WHITE)

    def update_location(self, location):
        '''
        Update only location
        '''
        self.location = self.font.render(
            str(location[0]) + ', ' + str(location[1]),
            False,
            WHITE)

    def update_time(self, time):
        '''
        Update only time
        '''
        self.time = self.font.render(
            format_time(time),
            False,
            WHITE)

    def update_date(self, date):
        '''
        Update only date
        '''
        self.date = self.font.render(
            str(date[0]) + ' ' + str(date[1]),
            False,
            WHITE)

    def update_turn_count(self, turn_count):
        '''
        Update only turn_count
        '''
        # TODO: Create colon character
        self.turn_count = self.font.render(
            "Turn " + str(turn_count),
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
        # Blit the time info
        self.surface.blit(self.time, (BORDER_WIDTH * 6,
                                      3 * self.font.get_linesize() +
                                      3 * LINE_SPACING +
                                      (BORDER_WIDTH * 4)))
        # Blit the date info
        self.surface.blit(self.date, (BORDER_WIDTH * 6,
                                      4 * self.font.get_linesize() +
                                      4 * LINE_SPACING +
                                      (BORDER_WIDTH * 4)))
        # Blit the turn info
        self.surface.blit(self.turn_count, (BORDER_WIDTH * 6,
                                            5 * self.font.get_linesize() +
                                            5 * LINE_SPACING +
                                            (BORDER_WIDTH * 4)))
        # Blit this hud's surface to the main hud surface
        surface_hud.blit(self.surface, (0, 0))
