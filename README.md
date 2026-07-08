# Keke's Game Collection

A terminal-based game suite for Linux, built with Python 3 and the curses library.

## Features

- **Clean ASCII Art Interface**: Beautiful header with "Keke's Game Collection"
- **Interactive Menu**: Navigate games using UP/DOWN arrow keys
- **Visual Feedback**: Selected games are highlighted with color
- **Easy Expansion**: Modular architecture makes adding new games simple

## Current Games (Phase 1)

1. **Tic Tac Toe** - Classic 3x3 grid game for two players
2. **Guess the Number** - Guess a number between 1 and 100
3. **Hangman** - Guess the word before the hangman is complete

## Installation

### Option 1: Using the install script (Recommended)

```bash
cd /home/keke/Absolute\ dogshit\ coding\ projects/kekes-game-collection
bash install.sh
```

After installation, you can launch the game collection from anywhere with:
```bash
kekegames
```

### Option 2: Manual launch

```bash
cd /home/keke/Absolute\ dogshit\ coding\ projects/kekes-game-collection
python3 main.py
```

### Option 3: Create a manual alias

Add this to your `~/.bashrc` or `~/.zshrc`:
```bash
alias kekegames='cd /home/keke/Absolute\ dogshit\ coding\ projects/kekes-game-collection && python3 main.py'
```

Then run:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

## Controls

### Menu Navigation
- **UP/DOWN Arrow Keys**: Navigate through the game list
- **ENTER**: Launch the selected game
- **Q**: Quit the game collection

### Game Controls
- Each game has its own controls displayed on screen
- Press **Q** in any game to return to the menu

## Adding New Games

The architecture is designed for easy expansion. To add a new game:

1. Create a new file in the `games/` directory (e.g., `newgame.py`)
2. Inherit from the `Game` base class
3. Implement the required methods:
   - `name`: Return the game's display name
   - `description`: Return a short description
   - `play(stdscr)`: Main game loop using curses

Example:
```python
from games.base import Game

class NewGame(Game):
    @property
    def name(self) -> str:
        return "My New Game"
    
    @property
    def description(self) -> str:
        return "A description of my game"
    
    def play(self, stdscr):
        # Your game logic here
        pass
```

4. Import and add your game to the `GameMenu` class in `menu.py`:
```python
from games import NewGame

# In __init__ method:
self.games = [
    TicTacToe(),
    GuessTheNumber(),
    Hangman(),
    NewGame()  # Add your game here
]
```

## Project Structure

```
kekes-game-collection/
├── main.py           # Entry point
├── menu.py           # Menu system
├── install.sh        # Installation script
├── README.md         # This file
└── games/
    ├── __init__.py   # Game imports
    ├── base.py       # Abstract base class
    ├── tictactoe.py  # Tic Tac Toe implementation
    ├── guessnumber.py # Guess the Number implementation
    └── hangman.py    # Hangman implementation
```

## Requirements

- Python 3.6 or higher
- Linux terminal with curses support
- No external dependencies (uses only Python standard library)

## Roadmap

- Phase 1: ✓ Core architecture + 3 games (Current)
- Phase 2: Add more games (target: 10 games)
- Phase 3: Add score tracking and high scores
- Phase 4: Add difficulty levels
- Phase 5: Reach 100 games!

## License

Free to use and modify for personal enjoyment.
