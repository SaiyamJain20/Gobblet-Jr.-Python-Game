# pylint: disable=no-member
"""Player class for the Gobblet Jr. game."""
from .piece import Piece

class Player:
    """
    Represents a player in Gobblet Jr. game.
    Manages the player's reserve pieces and color.
    """
    def __init__(self, color):
        """
        Initialize a player with the given color.
        """
        self.color = color
        self.reserve = []
        self.initialize_pieces()

    def initialize_pieces(self):
        """
        Initialize the player's reserve pieces: 2 of each size.
        """
        self.reserve = [
            Piece(self.color, 2), Piece(self.color, 2),  # Large
            Piece(self.color, 1), Piece(self.color, 1),  # Medium
            Piece(self.color, 0), Piece(self.color, 0)   # Small
        ]

    def get_piece_of_size(self, size):
        """
        Get a piece of the specified size from the reserve.
        """
        for piece in self.reserve:
            if piece.size == size:
                return piece
        return None

    def remove_from_reserve(self, piece):
        """
        Remove a piece from the reserve.
        """
        if piece in self.reserve:
            self.reserve.remove(piece)
            return True
        return False

    def count_pieces_of_size(self, size):
        """
        Count the number of pieces of a given size in the reserve.
        """
        return sum(1 for piece in self.reserve if piece.size == size)
