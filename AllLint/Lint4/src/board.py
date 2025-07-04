# pylint: disable=no-member
"""Board class for the Gobblet Jr. game."""
from .constants import BOARD_SIZE

class Board:
    """
    Represents the game board for Gobblet Jr.
    Manages the 3x3 grid of piece stacks and provides methods to interact with them.
    """
    def __init__(self):
        """
        Initialize an empty board.
        """
        # Initialize board (3x3 grid of stacks)
        self.grid = [[[] for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.last_move = None

    def reset(self):
        """
        Reset the board to its initial empty state.
        """
        self.grid = [[[] for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.last_move = None

    def get_top_piece(self, row, col):
        """
        Get the top piece at the specified board position.
        """
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.grid[row][col]:
            return self.grid[row][col][-1]
        return None

    def is_valid_move(self, piece, row, col):
        """
        Check if placing the piece at the given position is valid.
        """
        if not (0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE):
            return False

        top_piece = self.get_top_piece(row, col)
        return top_piece is None or piece.is_larger_than(top_piece)

    def place_piece(self, piece, row, col):
        """
        Place a piece on the board.
        """
        self.grid[row][col].append(piece)
        piece.position = (row, col)
        self.last_move = (row, col)

    def remove_piece(self, row, col):
        """
        Remove the top piece from the specified position.
        """
        if self.grid[row][col]:
            return self.grid[row][col].pop()
        return None

    def is_full(self):
        """
        Check if all spaces on the board are filled.
        """
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if not self.get_top_piece(row, col):
                    return False
        return True
