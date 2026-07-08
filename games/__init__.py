"""Game modules for Keke's Game Collection."""
from .base import Game
from .tictactoe import TicTacToe
from .guessnumber import GuessTheNumber
from .hangman import Hangman
from .rockpaperscissors import RockPaperScissors
from .blackjack import Blackjack
from .wordle import Wordle
from .dicebet import DiceBet

__all__ = ['Game', 'TicTacToe', 'GuessTheNumber', 'Hangman', 'RockPaperScissors', 'Blackjack', 'Wordle', 'DiceBet']
