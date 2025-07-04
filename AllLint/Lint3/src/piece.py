"""Piece class for the Gobblet Jr. game."""
import pygame
from .constants import BLACK, RED, RED_TRANSPARENT, BLUE_TRANSPARENT, PIECE_SIZES

class Piece:
    """
    Represents a single game piece with color and size attributes.
    """
    def __init__(self, color, size):
        """
        Initialize a game piece.
        """
        self.color = color  # RED or BLUE
        self.size = size  # 0 (small), 1 (medium), 2 (large)
        self.selected = False
        self.position = None  # (x, y) on board or None if in reserve

    def is_larger_than(self, other_piece):
        """
        Check if this piece is larger than another piece.
        """
        return other_piece is None or self.size > other_piece.size

    def draw(self, screen, x_coordinate, y_coordinate, transparent=False):
        """
        Draw the piece on the screen at the specified position.
        """
        color = self.color
        if transparent:
            if self.color == RED:
                color = RED_TRANSPARENT
            else:
                color = BLUE_TRANSPARENT
        pygame.draw.circle(screen, color, (x_coordinate, y_coordinate), PIECE_SIZES[self.size])
        pygame.draw.circle(screen, BLACK, (x_coordinate, y_coordinate), PIECE_SIZES[self.size], 2)
        # Draw a small black circle in the middle for visual distinction
        if self.size > 0:  # For medium and large pieces
            pygame.draw.circle(screen, BLACK, (x_coordinate, y_coordinate), 5)
