# pylint: disable=no-member
# pylint: disable=too-many-branches
"""Renderer for the Gobblet Jr. game."""
import pygame
from ..constants import (SCREEN_WIDTH, SCREEN_HEIGHT, BOARD_SIZE, SQUARE_SIZE,
                      BOARD_OFFSET_X, BOARD_OFFSET_Y, RESERVE_OFFSET_X,
                      RESERVE_OFFSET_Y, RESERVE_SLOT_HEIGHT, RESERVE_SLOT_WIDTH,
                      WHITE, BLACK, GREY, RED, BLUE, HIGHLIGHT, BACKGROUND,
                      LINE_COLOR, SLOT_COLOR, SLOT_BORDER)
from ..enums import GameState

class Renderer:
    """
    Handles all rendering for the Gobblet Jr. game.
    Responsible for drawing the board, pieces, and UI elements.
    """
    def __init__(self, screen):
        """
        Initialize the renderer.
        """
        self.screen = screen
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        self.size_labels = ["S", "M", "L"]

    def draw_game(self, game):
        """
        Draw the entire game state.
        """
        # Fill the background
        self.screen.fill(BACKGROUND)

        # Draw the board
        self._draw_board(game.board, game.selected_piece, game.valid_moves)

        # Draw reserve areas with vertical slots
        self._draw_reserve_area(RED, game.red_player.reserve)
        self._draw_reserve_area(BLUE, game.blue_player.reserve)

        # Draw player labels for reserve areas
        self._draw_player_labels()

        # Draw game status
        self._draw_game_status(game.current_state)

        # Draw instructions
        self._draw_instructions()

        self.draw_piece(game)

    def draw_piece(self, game):
        """
        Draw selected piece with mouse if one is selected
        """
        if game.selected_piece:
            mouse_pos = pygame.mouse.get_pos()
            game.selected_piece.draw(self.screen, mouse_pos[0], mouse_pos[1], transparent=True)

    def _draw_board(self, board, selected_piece, valid_moves):
        """
        Draw the game board and pieces.
        """
        # Draw the board background
        pygame.draw.rect(self.screen, WHITE,
                        (BOARD_OFFSET_X, BOARD_OFFSET_Y,
                         BOARD_SIZE * SQUARE_SIZE, BOARD_SIZE * SQUARE_SIZE))

        # Draw grid lines
        for i in range(BOARD_SIZE + 1):
            # Horizontal lines
            pygame.draw.line(self.screen, LINE_COLOR,
                           (BOARD_OFFSET_X, BOARD_OFFSET_Y + i * SQUARE_SIZE),
                           (BOARD_OFFSET_X + BOARD_SIZE * SQUARE_SIZE,
                            BOARD_OFFSET_Y + i * SQUARE_SIZE),
                           2)
            # Vertical lines
            pygame.draw.line(self.screen, LINE_COLOR,
                           (BOARD_OFFSET_X + i * SQUARE_SIZE, BOARD_OFFSET_Y),
                           (BOARD_OFFSET_X + i * SQUARE_SIZE,
                            BOARD_OFFSET_Y + BOARD_SIZE * SQUARE_SIZE),
                           2)

        # Highlight the last move
        if board.last_move:
            row, col = board.last_move
            pygame.draw.rect(self.screen, GREY,
                           (BOARD_OFFSET_X + col * SQUARE_SIZE,
                            BOARD_OFFSET_Y + row * SQUARE_SIZE,
                            SQUARE_SIZE, SQUARE_SIZE))

        # Highlight valid moves for selected piece
        if selected_piece:
            for row, col in valid_moves:
                pygame.draw.rect(self.screen, HIGHLIGHT,
                               (BOARD_OFFSET_X + col * SQUARE_SIZE,
                                BOARD_OFFSET_Y + row * SQUARE_SIZE,
                                SQUARE_SIZE, SQUARE_SIZE))

        # Draw pieces on the board
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                square_center_x = BOARD_OFFSET_X + col * SQUARE_SIZE + SQUARE_SIZE // 2
                square_center_y = BOARD_OFFSET_Y + row * SQUARE_SIZE + SQUARE_SIZE // 2

                piece = board.get_top_piece(row, col)
                if piece:
                    piece.draw(self.screen, square_center_x, square_center_y)

    def _draw_reserve_area(self, color, reserves):
        """
        Draw reserve area for the specified color.
        """
        # Position differs based on player color
        is_blue = color == BLUE
        if is_blue:
            base_x = SCREEN_WIDTH - RESERVE_OFFSET_X - RESERVE_SLOT_WIDTH
        else:
            base_x = RESERVE_OFFSET_X

        # Draw slots for each size (L, M, S)
        for i, size in enumerate([2, 1, 0]):
            # Draw slot
            slot_x = base_x
            slot_y = RESERVE_OFFSET_Y + i * RESERVE_SLOT_HEIGHT
            pygame.draw.rect(self.screen, SLOT_COLOR,
                           (slot_x, slot_y, RESERVE_SLOT_WIDTH, RESERVE_SLOT_HEIGHT))
            pygame.draw.rect(self.screen, SLOT_BORDER,
                           (slot_x, slot_y, RESERVE_SLOT_WIDTH, RESERVE_SLOT_HEIGHT), 2)

            # Draw size label
            size_label = self.small_font.render(self.size_labels[size], True, BLACK)
            self.screen.blit(size_label, (slot_x + 10, slot_y + 5))

            # Draw counter for how many pieces of this size are in reserve
            count = sum(1 for piece in reserves if piece.size == size)
            count_label = self.small_font.render(f"x{count}", True, color)
            self.screen.blit(count_label, (slot_x + RESERVE_SLOT_WIDTH - 30, slot_y + 5))

            # Draw the pieces in this slot
            for piece in reserves:
                if piece.size == size:
                    piece_x = slot_x + RESERVE_SLOT_WIDTH // 2
                    piece_y = slot_y + RESERVE_SLOT_HEIGHT // 2
                    piece.draw(self.screen, piece_x, piece_y)
                    break  # Just draw one piece per slot as representative

    def _draw_player_labels(self):
        """
        Draw player labels for reserve areas.
        """
        red_label = self.font.render("RED PIECES", True, RED)
        blue_label = self.font.render("BLUE PIECES", True, BLUE)
        self.screen.blit(red_label, (RESERVE_OFFSET_X, RESERVE_OFFSET_Y - 50))
        self.screen.blit(blue_label, (SCREEN_WIDTH - RESERVE_OFFSET_X
                                     - blue_label.get_width(), RESERVE_OFFSET_Y - 50))

    def _draw_game_status(self, current_state):
        """
        Draw the current game status.
        """
        status_text = ""
        text_color = BLACK

        if current_state == GameState.PLAYER_RED:
            status_text = "Red's Turn"
            text_color = RED
        elif current_state == GameState.PLAYER_BLUE:
            status_text = "Blue's Turn"
            text_color = BLUE
        elif current_state == GameState.RED_WIN:
            status_text = "Red Wins!"
            text_color = RED
        elif current_state == GameState.BLUE_WIN:
            status_text = "Blue Wins!"
            text_color = BLUE
        elif current_state == GameState.DRAW:
            status_text = "Draw!"
            text_color = BLACK

        status_surface = self.font.render(status_text, True, text_color)
        self.screen.blit(status_surface, (SCREEN_WIDTH // 2 - status_surface.get_width() // 2, 30))

    def _draw_instructions(self):
        """
        Draw game instructions.
        """
        instructions = "Click on a piece slot to select, then click on a valid square to move"
        instructions_surface = self.small_font.render(instructions, True, BLACK)
        self.screen.blit(instructions_surface,
                        (SCREEN_WIDTH // 2 - instructions_surface.get_width() // 2, 70))

        reset_text = "Press 'R' to reset the game"
        reset_surface = self.small_font.render(reset_text, True, BLACK)
        self.screen.blit(reset_surface,
                        (SCREEN_WIDTH // 2 - reset_surface.get_width() // 2, SCREEN_HEIGHT - 30))
