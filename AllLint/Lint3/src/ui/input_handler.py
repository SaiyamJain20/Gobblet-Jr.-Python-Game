"""Input handler for the Gobblet Jr. game."""
import pygame
from ..constants import (BOARD_SIZE, SQUARE_SIZE, BOARD_OFFSET_X, BOARD_OFFSET_Y,
                     RESERVE_OFFSET_X, RESERVE_OFFSET_Y, RESERVE_SLOT_HEIGHT,
                     RESERVE_SLOT_WIDTH, SCREEN_WIDTH, RED)
from ..enums import GameState

class InputHandler:
    """
    Handles all user input for the Gobblet Jr. game.
    Processes mouse clicks and keyboard events.
    """
    def __init__(self, game):
        """
        Initialize the input handler.
        """
        self.game = game

    def handle_events(self):
        """
        Handle pygame events (quit, key presses, mouse clicks).
        """
        quit_game = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.game.reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    self.handle_click(mouse_pos)
        if quit_game:
            return False
        return True

    def handle_click(self, mouse_pos):
        """
        Handle mouse click events based on current game state.
        """
        # If game is over, only allow reset
        if self.game.current_state in [GameState.RED_WIN, GameState.BLUE_WIN, GameState.DRAW]:
            return

        current_player = self.game.get_current_player()

        # If a piece is already selected, only allow clicking on valid move positions
        if self.game.selected_piece:
            self._try_place_selected_piece(mouse_pos)
            return

        # Only when no piece is selected, check reserve or board for selecting a piece
        reserve_clicked = self._check_reserve_click(mouse_pos, current_player)
        if not reserve_clicked:
            self._check_board_click(mouse_pos, current_player)

    def _try_place_selected_piece(self, mouse_pos):
        """
        Try to place the currently selected piece at the clicked position.
        """
        # Check if click is on the board
        if (BOARD_OFFSET_X <= mouse_pos[0] <= BOARD_OFFSET_X + BOARD_SIZE * SQUARE_SIZE and
            BOARD_OFFSET_Y <= mouse_pos[1] <= BOARD_OFFSET_Y + BOARD_SIZE * SQUARE_SIZE):

            # Calculate which square was clicked
            col = int((mouse_pos[0] - BOARD_OFFSET_X) // SQUARE_SIZE)
            row = int((mouse_pos[1] - BOARD_OFFSET_Y) // SQUARE_SIZE)

            # Try to make the move
            self.game.make_move(row, col)

    def _check_reserve_click(self, mouse_pos, current_player):
        """
        Check if a reserve piece was clicked.
        """
        is_red = current_player.color == RED
        if is_red:
            base_x = RESERVE_OFFSET_X
        else:
            base_x = SCREEN_WIDTH - RESERVE_OFFSET_X - RESERVE_SLOT_WIDTH

        for i, size in enumerate([2, 1, 0]):  # Large, Medium, Small
            slot_x = base_x
            slot_y = RESERVE_OFFSET_Y + i * RESERVE_SLOT_HEIGHT
            slot_width = RESERVE_SLOT_WIDTH
            slot_height = RESERVE_SLOT_HEIGHT

            # Check if click is within this slot
            if (slot_x <= mouse_pos[0] <= slot_x + slot_width and
                slot_y <= mouse_pos[1] <= slot_y + slot_height):
                # Find if there's a piece of this size in reserve
                piece = current_player.get_piece_of_size(size)
                if piece:
                    self.game.select_piece(piece)
                    return True
        return False

    def _check_board_click(self, mouse_pos, current_player):
        """
        Check if a board square was clicked.
        """
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                # Check if the click is within this square
                if (BOARD_OFFSET_X + col * SQUARE_SIZE <= mouse_pos[0] <=
                    BOARD_OFFSET_X + (col + 1) * SQUARE_SIZE and
                    BOARD_OFFSET_Y + row * SQUARE_SIZE <= mouse_pos[1] <=
                    BOARD_OFFSET_Y + (row + 1) * SQUARE_SIZE):

                    # Try to select a piece on the board
                    piece = self.game.board.get_top_piece(row, col)
                    if piece and piece.color == current_player.color:
                        self.game.select_piece(piece)
                        return
