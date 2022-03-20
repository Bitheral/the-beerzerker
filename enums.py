"""
Author:  Nathan Dow / Bitheral
Created: 24/10/2020
"""
from enum import Enum

# Screens list
# All possible screens to exist
class Screens(Enum):
    SPLASHSCREEN = -1
    MAIN_MENU = 0
    SETTINGS = 1
    CREDITS = 2
    QUIT = 3
    GAME = 4
    SOUND_WARNING = 5


# Direction list
# All possible directions to exit
# Needed for player attack
class Direction(Enum):
    UP = 0
    DOWN = 180
    LEFT = 90
    RIGHT = 270
    UP_LEFT = 45
    UP_RIGHT = 315
    DOWN_LEFT = 135
    DOWN_RIGHT = 225

# Scene list
# All scenes in game
# Needed for portals
class Scenes(Enum):
    TUTORIAL = 0
    LEVEL_1 = 1
