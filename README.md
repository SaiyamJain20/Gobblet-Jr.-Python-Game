# Gobblet-Jr.-Python-Game

This project is a Python implementation of the board game Gobblet Jr. using the Pygame library. The game features a 3x3 board where each player (red and blue) has a reserve of 6 pieces (2 pieces of each size). All rules described in the provided references have been implemented, with design choices (e.g. using circles to represent pieces) made for clarity and simplicity.

## Functional Requirements and Assumptions

- **Board Setup:**  
  - The game board is a 3x3 grid. Pieces may be placed on any cell following the rule that a larger piece can cover a smaller piece.
  
- **Pieces:**  
  - Each player has 6 pieces (2 pieces of sizes 1, 2, and 3). Pieces are drawn as circles with radius proportional to their size.

- **Reserves and Moves:**  
  - Players have reserves (displayed on the screen) from which they can select pieces to move to the board. The game enforces that only a piece of larger size can cover a smaller one.

- **Winning Condition:**  
  - The game checks rows, columns, and diagonals for a win (all cells in a line having a top piece of the same owner).

- **Design Assumptions:**  
  - The game uses a fixed window size of 600x850 pixels.
  - Colors, spacing, and other visual elements have been chosen for clarity.
  - All rules as per the game document and online resources have been implemented.
  
- **User Interaction:**  
  - The game is controlled via mouse clicks. Pieces are selected either from the reserve or from the board if they belong to the current player. A valid move is determined by comparing piece sizes.

## Running the Game and Tests

### How to run

```
python3 gobblet.py
```

### How to pylint

```
pylint gobblet.py src/player.py src/piece.py src/game.py src/enums.py src/constants.py src/board.py src/ui/input_handler.py src/ui/renderer.py src/ui/ui_components.py
```
