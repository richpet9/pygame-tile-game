'''
Constant values throughout the program
'''
from tcod.constants import FOV_SHADOW

# SIZES OF THINGS IN PIXELS
DISPLAY_WIDTH = 1408
DISPLAY_HEIGHT = 792
CELL_WIDTH = 32
CELL_HEIGHT = 32
CAMERA_WIDTH = (DISPLAY_WIDTH * 3) // 5
CAMERA_HEIGHT = DISPLAY_HEIGHT

# SIZES OF THINGS IN CELLS
MAP_WIDTH = 64
MAP_HEIGHT = 1024
DISPLAY_WIDTH_CELL = DISPLAY_WIDTH // CELL_WIDTH
DISPLAY_HEIGHT_CELL = DISPLAY_HEIGHT // CELL_HEIGHT
CAMERA_WIDTH_CELL = CAMERA_WIDTH // CELL_WIDTH
CAMERA_HEIGHT_CELL = CAMERA_HEIGHT // CELL_HEIGHT

# FOV
FOV_RADIUS = 20  # IN CELLS
FOV_ALG = FOV_SHADOW

# TIMES
MINUTES_PER_TURN = 5
