"""Wordle game implementation."""
import curses
import random
from .base import Game


class Wordle(Game):
    """Wordle-style word guessing game."""
    
    WORDS = [
        "apple", "beach", "brain", "bread", "brush", "chair", "chest", "chord",
        "click", "clock", "cloud", "dance", "diary", "drink", "drive", "earth",
        "feast", "field", "fruit", "glass", "grape", "green", "ghost", "heart",
        "horse", "house", "juice", "light", "lemon", "melon", "money", "music",
        "night", "ocean", "party", "phone", "piano", "pilot", "plane", "plant",
        "plate", "power", "radio", "river", "robot", "shirt", "shoes", "skate",
        "slide", "snake", "space", "spoon", "stack", "stage", "stand", "start",
        "stone", "storm", "sugar", "table", "taste", "tiger", "toast", "touch",
        "tower", "track", "trade", "train", "treat", "truck", "trust", "uncle",
        "video", "voice", "waste", "watch", "water", "whale", "wheat", "wheel",
        "where", "while", "white", "whole", "woman", "world", "write", "wrong",
        "yacht", "youth", "zebra"
    ]
    
    @property
    def name(self) -> str:
        return "Wordle"
    
    @property
    def description(self) -> str:
        return "Guess the 5-letter word in 6 attempts"
    
    def play(self, stdscr):
        """Main game loop for Wordle."""
        curses.curs_set(1)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        
        h, w = stdscr.getmaxyx()
        
        secret = random.choice(self.WORDS)
        guesses = []
        current_guess = ""
        game_over = False
        won = False
        
        while not game_over:
            self.draw_game(stdscr, guesses, current_guess, won, secret, h, w)
            
            if game_over:
                # Game over loop - wait for Q to quit
                while True:
                    key = stdscr.getch()
                    if key == ord('q'):
                        break
                break
            
            # Handle input
            key = stdscr.getch()
            
            if key == curses.KEY_ENTER or key in [10, 13]:
                if len(current_guess) == 5:
                    guesses.append(current_guess)
                    if current_guess == secret:
                        won = True
                        game_over = True
                    elif len(guesses) >= 6:
                        game_over = True
                    current_guess = ""
            elif key == curses.KEY_BACKSPACE or key == 127:
                current_guess = current_guess[:-1]
            elif key == ord('q'):
                break
            elif 97 <= key <= 122:  # Lowercase a-z
                if len(current_guess) < 5:
                    current_guess += chr(key)
    
    def draw_game(self, stdscr, guesses, current_guess, won, secret, h, w):
        """Draw the game interface."""
        stdscr.clear()
        
        # Title
        title = "WORDLE"
        stdscr.addstr(2, (w - len(title)) // 2, title, curses.A_BOLD | curses.color_pair(1))
        
        # Draw guesses
        start_y = 6
        for i in range(6):
            if i < len(guesses):
                guess = guesses[i]
                self.draw_guess(stdscr, guess, secret, start_y + i * 2, w)
            elif i == len(guesses):
                # Current guess being typed
                self.draw_current_guess(stdscr, current_guess, start_y + i * 2, w)
            else:
                # Empty row
                self.draw_empty_row(stdscr, start_y + i * 2, w)
        
        # Result display
        if won:
            result_y = start_y + 12
            msg = "YOU WON! Press 'Q' to return to menu"
            stdscr.addstr(result_y, (w - len(msg)) // 2, msg, curses.color_pair(3) | curses.A_BOLD)
            word_msg = f"The word was: {secret}"
            stdscr.addstr(result_y + 1, (w - len(word_msg)) // 2, word_msg, curses.color_pair(2))
        elif len(guesses) >= 6:
            result_y = start_y + 12
            msg = "YOU FAILED! Press 'Q' to return to menu"
            stdscr.addstr(result_y, (w - len(msg)) // 2, msg, curses.color_pair(4) | curses.A_BOLD)
            word_msg = f"The word was: {secret}"
            stdscr.addstr(result_y + 1, (w - len(word_msg)) // 2, word_msg, curses.color_pair(2))
        else:
            stdscr.addstr(start_y + 12, (w - 30) // 2, "Type a 5-letter word, ENTER to submit", curses.color_pair(2))
        
        # Legend
        legend_y = start_y + 14
        stdscr.addstr(legend_y, (w - 40) // 2, "Green: Correct | Yellow: Wrong position | Gray: Not in word", curses.A_DIM)
        
        # Footer
        footer = "Press Q to quit to menu"
        stdscr.addstr(h - 2, (w - len(footer)) // 2, footer, curses.A_DIM)
        
        stdscr.refresh()
    
    def draw_guess(self, stdscr, guess, secret, y, w):
        """Draw a completed guess with color feedback."""
        start_x = (w - 15) // 2
        
        # Track which letters have been used in secret
        secret_letters = list(secret)
        
        for i, letter in enumerate(guess):
            x = start_x + i * 3
            
            if letter == secret[i]:
                # Correct position - green
                stdscr.addstr(y, x, f"[{letter}]", curses.color_pair(3) | curses.A_BOLD)
                secret_letters[i] = None  # Mark as used
            elif letter in secret_letters:
                # Wrong position - yellow
                stdscr.addstr(y, x, f"[{letter}]", curses.color_pair(1) | curses.A_BOLD)
                # Remove first occurrence
                idx = secret_letters.index(letter)
                secret_letters[idx] = None
            else:
                # Not in word - gray
                stdscr.addstr(y, x, f"[{letter}]", curses.A_DIM)
    
    def draw_current_guess(self, stdscr, guess, y, w):
        """Draw the current guess being typed."""
        start_x = (w - 15) // 2
        
        for i in range(5):
            x = start_x + i * 3
            if i < len(guess):
                stdscr.addstr(y, x, f"[{guess[i]}]", curses.color_pair(6) | curses.A_BOLD)
            else:
                stdscr.addstr(y, x, "[_]", curses.A_NORMAL)
    
    def draw_empty_row(self, stdscr, y, w):
        """Draw an empty row."""
        start_x = (w - 15) // 2
        
        for i in range(5):
            x = start_x + i * 3
            stdscr.addstr(y, x, "[_]", curses.A_DIM)
