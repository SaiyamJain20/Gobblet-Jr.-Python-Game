# pylint: disable=no-member
"""
Made By - Saiyam Jain
Gobblet Jr. Board Game - Main Entry Point.

A strategic board game where players place and move pieces of different sizes
on a 3x3 grid, with the goal of creating a line of their colored pieces.

To run the game:
    python3 gobblet.py
"""

import sys
import pygame
from src.game import GobbletJr

def main():
    """
    Main entry point function.
    """
    # Initialize pygame
    pygame.init()

    try:
        # Create and run the game
        game = GobbletJr()
        game.run()
    except Exception as exception:  # pylint: disable=broad-except
        print(f"An error occurred: {exception}")
        return 1
    finally:
        # Clean up pygame
        pygame.quit()

    return 0

if __name__ == "__main__":
    sys.exit(main())
