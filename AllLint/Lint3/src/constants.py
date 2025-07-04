"""Constants for the Gobblet Jr. game."""
import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Board configuration
BOARD_SIZE = 3
SQUARE_SIZE = 140
BOARD_OFFSET_X = (SCREEN_WIDTH - BOARD_SIZE * SQUARE_SIZE) // 2
BOARD_OFFSET_Y = (SCREEN_HEIGHT - BOARD_SIZE * SQUARE_SIZE) // 2

# Piece sizes (radius in pixels)
PIECE_SIZES = [20, 40, 60]

# Reserve configuration
RESERVE_OFFSET_X = 100
RESERVE_OFFSET_Y = 150
RESERVE_SLOT_HEIGHT = 150
RESERVE_SLOT_WIDTH = 150

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
RED_TRANSPARENT = (255, 0, 0, 128)
BLUE_TRANSPARENT = (0, 0, 255, 128)
HIGHLIGHT = (255, 255, 0, 150)
BACKGROUND = (240, 240, 220)
LINE_COLOR = (50, 50, 50)
SLOT_COLOR = (230, 230, 230)
SLOT_BORDER = (180, 180, 180)
