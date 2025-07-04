"""Main game class for the Gobblet Jr. board game."""
import pygame
from .constants import RED, BLUE, SCREEN_WIDTH, SCREEN_HEIGHT
from .enums import GameState
from .board import Board
from .player import Player
from .ui.renderer import Renderer
from .ui.input_handler import InputHandler

class GobbletJr:
    """
    Main game class for the Gobblet Jr. board game.
    Manages game state, board, pieces, and interactions.
    """
    def __init__(self):
        """
        Initialize the game with default settings and UI elements.
        """
        # Initialize pygame
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Gobblet Jr.")
        self.clock = pygame.time.Clock()

        # Create components
        self.board = Board()
        self.red_player = Player(RED)
        self.blue_player = Player(BLUE)
        self.renderer = Renderer(self.screen)
        self.input_handler = InputHandler(self)

        # Game state
        self.selected_piece = None
        self.valid_moves = []
        self.current_state = GameState.PLAYER_RED

    def reset_game(self):
        """
        Reset the game to its initial state.
        """
        # Reset board
        self.board.reset()

        # Reset players
        self.red_player.initialize_pieces()
        self.blue_player.initialize_pieces()

        # Reset game state
        self.current_state = GameState.PLAYER_RED
        self.selected_piece = None
        self.valid_moves = []

    def get_current_player(self):
        """
        Get the current player object.
        """
        if self.current_state == GameState.PLAYER_RED:
            return self.red_player
        return self.blue_player

    def select_piece(self, piece):
        """
        Select a piece and calculate its valid moves.
        """
        # Deselect previously selected piece
        if self.selected_piece:
            self.selected_piece.selected = False

        # Select new piece
        piece.selected = True
        self.selected_piece = piece

        # Calculate valid moves
        self.valid_moves = self._get_valid_moves(piece)

    def _get_valid_moves(self, piece):
        """
        Calculate all valid board positions for the selected piece.
        """
        valid_moves = []

        # If the piece is in reserve, it can be placed on any valid square
        if piece.position is None:
            for row in range(3):
                for col in range(3):
                    if self.board.is_valid_move(piece, row, col):
                        # Check if this move would reveal a winning line for the opponent
                        if not self._would_reveal_win_for_opponent(piece, None, row, col):
                            valid_moves.append((row, col))
        else:
            # If piece is on the board, it can be moved to any valid square
            current_row, current_col = piece.position

            for row in range(3):
                for col in range(3):
                    # Can't move to the same position
                    if (row, col) == (current_row, current_col):
                        continue

                    if self.board.is_valid_move(piece, row, col):
                        # Check if this move would reveal a winning line for the opponent
                        # if not self._would_reveal_win_for_opponent(piece, piece.position, row, col):
                        valid_moves.append((row, col))

        return valid_moves

    def _would_reveal_win_for_opponent(self, piece, from_pos, to_row, to_col):
        """
        Check if moving a piece would reveal a winning line for the opponent.
        """
        # Create a copy of the board to simulate the move
        temp_board = [[stack.copy() for stack in row] for row in self.board.grid]

        # Remove the piece from its current position if it's on the board
        if from_pos:
            from_row, from_col = from_pos
            if temp_board[from_row][from_col] and temp_board[from_row][from_col][-1] == piece:
                temp_board[from_row][from_col].pop()

        # Check if removing the piece reveals a win for the opponent
        opponent_color = BLUE if piece.color == RED else RED

        # Check rows
        for row in range(3):
            count = 0
            for col in range(3):
                top_piece = None
                if temp_board[row][col]:
                    top_piece = temp_board[row][col][-1]
                if top_piece and top_piece.color == opponent_color:
                    count += 1
                else:
                    break
            if count == 3:
                return True

        # Check columns
        for col in range(3):
            count = 0
            for row in range(3):
                top_piece = None
                if temp_board[row][col]:
                    top_piece = temp_board[row][col][-1]
                if top_piece and top_piece.color == opponent_color:
                    count += 1
                else:
                    break
            if count == 3:
                return True

        # Check diagonals
        count = 0
        for i in range(3):
            top_piece = None
            if temp_board[i][i]:
                top_piece = temp_board[i][i][-1]
            if top_piece and top_piece.color == opponent_color:
                count += 1
            else:
                break
        if count == 3:
            return True

        count = 0
        for i in range(3):
            top_piece = None
            if temp_board[i][2 - i]:
                top_piece = temp_board[i][2 - i][-1]
            if top_piece and top_piece.color == opponent_color:
                count += 1
            else:
                break
        if count == 3:
            return True

        return False

    def make_move(self, row, col):
        """
        Make a move with the selected piece to the specified position.
        """
        if not self.selected_piece or (row, col) not in self.valid_moves:
            return False

        # If piece is coming from the board, remove it from its current position
        if self.selected_piece.position:
            from_row, from_col = self.selected_piece.position
            self.board.remove_piece(from_row, from_col)
        else:
            # If piece is coming from reserve, remove it from reserve
            current_player = self.get_current_player()
            current_player.remove_from_reserve(self.selected_piece)

        # Add piece to the new position
        self.board.place_piece(self.selected_piece, row, col)

        # Deselect the piece and clear valid moves
        self.selected_piece.selected = False
        self.selected_piece = None
        self.valid_moves = []

        # Check for win conditions
        if self._check_win(RED):
            self.current_state = GameState.RED_WIN
        elif self._check_win(BLUE):
            self.current_state = GameState.BLUE_WIN
        elif self.board.is_full():
            self.current_state = GameState.DRAW
        else:
            # Switch players
            if self.current_state == GameState.PLAYER_RED:
                self.current_state = GameState.PLAYER_BLUE
            else:
                self.current_state = GameState.PLAYER_RED

        return True

    def _check_win(self, color):
        """
        Check if the specified color has won the game.
        """
        # Check rows
        for row in range(3):
            if all(self.board.get_top_piece(row, col) and
                  self.board.get_top_piece(row, col).color == color for col in range(3)):
                return True

        # Check columns
        for col in range(3):
            if all(self.board.get_top_piece(row, col) and
                  self.board.get_top_piece(row, col).color == color for row in range(3)):
                return True

        # Check diagonals
        if all(self.board.get_top_piece(i, i) and
              self.board.get_top_piece(i, i).color == color for i in range(3)):
            return True

        if all(self.board.get_top_piece(i, 2 - i) and
              self.board.get_top_piece(i, 2 - i).color == color for i in range(3)):
            return True

        return False

    def run(self):
        """
        Run the main game loop.
        """
        running = True
        while running:
            running = self.input_handler.handle_events()
            self.renderer.draw_game(self)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
