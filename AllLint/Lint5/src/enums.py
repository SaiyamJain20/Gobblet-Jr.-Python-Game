# pylint: disable=no-member
# pylint: disable=too-many-branches
"""Game state enumerations for the Gobblet Jr. game."""
from enum import Enum, auto

class GameState(Enum):
    """
    Represents the possible states of the Gobblet game.
    """
    PLAYER_RED = auto()
    PLAYER_BLUE = auto()
    RED_WIN = auto()
    BLUE_WIN = auto()
    DRAW = auto()
