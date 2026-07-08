"""Base class for all games in the collection."""
from abc import ABC, abstractmethod


class Game(ABC):
    """Abstract base class for all games."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the display name of the game."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Return a short description of the game."""
        pass
    
    @abstractmethod
    def play(self, stdscr):
        """Main game loop. Receives curses stdscr object."""
        pass
