"""UI components for the Gobblet Jr. game."""
import pygame
from ..constants import (WHITE, BLACK, GREY)

class Button:
    """
    A clickable button component for the UI.
    Handles drawing and click detection.
    """
    def __init__(self, x_coordinate, y_coordinate, width, height, text,
                 color=WHITE, hover_color=GREY, text_color=BLACK):
        """
        Initialize a button.
        """
        self.rect = pygame.Rect(x_coordinate, y_coordinate, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, 30)
        self.is_hovered = False

    def draw(self, screen):
        """
        Draw the button on the screen.
        """
        # Determine color based on hover state
        current_color = self.hover_color if self.is_hovered else self.color

        # Draw button rectangle
        pygame.draw.rect(screen, current_color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)  # Border

        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def update(self, mouse_pos):
        """
        Update hover state based on mouse position.
        """
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos, mouse_click):
        """
        Check if the button was clicked.
        """
        return self.rect.collidepoint(mouse_pos) and mouse_click

class GameDialog:
    """
    A dialog box for displaying messages.
    Used for game state notifications and confirmations.
    """
    def __init__(self, width, height, message, title="Message"):
        """
        Initialize a dialog box.
        """
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (pygame.display.get_surface().get_width() // 2,
                          pygame.display.get_surface().get_height() // 2)
        self.title = title
        self.message = message
        self.title_font = pygame.font.SysFont(None, 36)
        self.message_font = pygame.font.SysFont(None, 28)
        self.ok_button = Button(
            self.rect.centerx - 50,
            self.rect.bottom - 60,
            100, 40, "OK", GREY, WHITE
        )
        self.visible = False

    def draw(self, screen):
        """
        Draw the dialog if visible.
        """
        if not self.visible:
            return

        # Semi-transparent background overlay
        overlay = pygame.Surface((pygame.display.get_surface().get_width(),
                                pygame.display.get_surface().get_height()),
                               pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        screen.blit(overlay, (0, 0))

        # Dialog background
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        # Title
        title_surface = self.title_font.render(self.title, True, BLACK)
        title_rect = title_surface.get_rect(
            center=(self.rect.centerx, self.rect.top + 30)
        )
        screen.blit(title_surface, title_rect)

        # Divider line
        pygame.draw.line(
            screen, GREY,
            (self.rect.left + 20, self.rect.top + 60),
            (self.rect.right - 20, self.rect.top + 60),
            2
        )

        # Message (support multi-line)
        lines = self.message.split('\n')
        for i, line in enumerate(lines):
            msg_surface = self.message_font.render(line, True, BLACK)
            msg_rect = msg_surface.get_rect(
                center=(self.rect.centerx, self.rect.top + 100 + i * 30)
            )
            screen.blit(msg_surface, msg_rect)

        # OK button
        self.ok_button.draw(screen)

    def update(self, mouse_pos):
        """
        Update dialog components.
        """
        if self.visible:
            self.ok_button.update(mouse_pos)

    def handle_click(self, mouse_pos):
        """
        Handle click event.
        """
        if self.visible and self.ok_button.is_clicked(mouse_pos, True):
            self.visible = False
            return True
        return False

class PieceCounter:
    """
    Visual counter for remaining reserve pieces.
    Displays how many pieces of each size a player has left.
    """
    def __init__(self, x_coordinate, y_coordinate, color):
        """
        Initialize the piece counter.
        """
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.color = color
        self.font = pygame.font.SysFont(None, 24)

    def draw(self, screen, piece_counts):
        """
        Draw the counter showing each piece size count.
        """

        for idx, size in enumerate(range(3)):
            count = piece_counts.get(size, 0)
            text_surface = self.label_render(count, idx)
            screen.blit(text_surface, (self.x_coordinate, self.y_coordinate + idx * 25))

    def label_render(self, count, idx):
        """
        Render the label for a piece size count.
        """
        labels = ["Small", "Medium", "Large"]
        label = f"{labels[idx]}: {count}"
        text_surface = self.font.render(label, True, self.color)
        return text_surface

class Timer:
    """
    Timer display for tracking player turns.
    Shows elapsed time for the current turn and total game time.
    """
    def __init__(self, x_coordinate, y_coordinate):
        """
        Initialize the timer.
        """
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.font = pygame.font.SysFont(None, 24)
        self.start_time = pygame.time.get_ticks()
        self.turn_start_time = self.start_time

    def reset_turn_timer(self):
        """
        Reset the turn timer.
        """
        self.turn_start_time = pygame.time.get_ticks()

    def draw(self, screen):
        """
        Draw the timer display.
        """
        current_time = pygame.time.get_ticks()

        # Calculate times in seconds
        total_time = (current_time - self.start_time) // 1000
        turn_time = (current_time - self.turn_start_time) // 1000

        # Format times as MM:SS
        total_time_str = f"{total_time // 60:02d}:{total_time % 60:02d}"
        turn_time_str = f"{turn_time // 60:02d}:{turn_time % 60:02d}"

        # Draw times
        total_label = f"Game Time: {total_time_str}"
        turn_label = f"Turn Time: {turn_time_str}"

        total_surface = self.font.render(total_label, True, BLACK)
        turn_surface = self.font.render(turn_label, True, BLACK)

        screen.blit(total_surface, (self.x_coordinate, self.y_coordinate))
        screen.blit(turn_surface, (self.x_coordinate, self.y_coordinate + 25))
