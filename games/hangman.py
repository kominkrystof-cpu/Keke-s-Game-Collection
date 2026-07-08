"""Hangman game implementation."""
import curses
import random
from .base import Game


class Hangman(Game):
    """Classic Hangman game."""
    
    WORDS = [
        "python", "linux", "terminal", "keyboard", "monitor",
        "programming", "developer", "software", "hardware", "network",
        "algorithm", "database", "function", "variable", "constant"
    ]
    
    @property
    def name(self) -> str:
        return "Hangman"
    
    @property
    def description(self) -> str:
        return "Guess the word before the hangman is complete"
    
    def play(self, stdscr):
        """Main game loop for Hangman."""
        curses.curs_set(0)
        h, w = stdscr.getmaxyx()
        
        # Initialize colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        
        word = random.choice(self.WORDS)
        guessed = set()
        wrong_guesses = []
        max_wrong = 6
        game_over = False
        won = False
        
        while not game_over:
            stdscr.clear()
            
            # Title
            title = "HANGMAN"
            stdscr.addstr(2, (w - len(title)) // 2, title, curses.A_BOLD | curses.color_pair(1))
            
            # Draw hangman
            self.draw_hangman(stdscr, len(wrong_guesses), w)
            
            # Display word
            display_word = " ".join(
                letter if letter in guessed else "_" for letter in word
            )
            stdscr.addstr(12, (w - len(display_word)) // 2, display_word, curses.A_BOLD)
            
            # Wrong guesses
            if wrong_guesses:
                wrong_str = f"Wrong: {', '.join(wrong_guesses)}"
                stdscr.addstr(14, (w - len(wrong_str)) // 2, wrong_str, curses.color_pair(4))
            
            # Game status
            if won:
                msg = "YOU WON! Press 'Q' to return to menu"
                stdscr.addstr(16, (w - len(msg)) // 2, msg, curses.color_pair(3) | curses.A_BOLD)
                word_msg = f"The word was: {word}"
                stdscr.addstr(17, (w - len(word_msg)) // 2, word_msg, curses.color_pair(2))
            elif len(wrong_guesses) >= max_wrong:
                msg = "YOU FAILED! Press 'Q' to return to menu"
                stdscr.addstr(16, (w - len(msg)) // 2, msg, curses.color_pair(4) | curses.A_BOLD)
                word_msg = f"The word was: {word}"
                stdscr.addstr(17, (w - len(word_msg)) // 2, word_msg, curses.color_pair(2))
            else:
                msg = "Guess a letter (A-Z)"
                stdscr.addstr(16, (w - len(msg)) // 2, msg, curses.color_pair(2))
            
            # Help
            stdscr.addstr(h - 2, (w - 30) // 2, "Press Q to quit", curses.A_DIM)
            
            stdscr.refresh()
            
            if game_over:
                # Game over loop - wait for Q to quit
                while True:
                    key = stdscr.getch()
                    if key == ord('q'):
                        break
                break
            
            # Handle input
            key = stdscr.getch()
            
            if key == ord('q'):
                break
            elif 97 <= key <= 122:  # Lowercase a-z
                letter = chr(key)
                if letter not in guessed and not game_over:
                    guessed.add(letter)
                    if letter not in word:
                        wrong_guesses.append(letter)
                    
                    # Check win condition
                    if all(letter in guessed for letter in word):
                        won = True
                        game_over = True
                    elif len(wrong_guesses) >= max_wrong:
                        game_over = True
    
    def draw_hangman(self, stdscr, wrong_count, w):
        """Draw the hangman figure based on wrong guesses."""
        base_x = (w - 10) // 2
        base_y = 4
        
        # Gallows (always drawn)
        stdscr.addstr(base_y, base_x + 4, "     ")
        stdscr.addstr(base_y + 1, base_x + 4, "     ")
        stdscr.addstr(base_y + 2, base_x, "_______")
        stdscr.addstr(base_y + 3, base_x, "|     |")
        stdscr.addstr(base_y + 4, base_x, "|")
        stdscr.addstr(base_y + 5, base_x, "|")
        stdscr.addstr(base_y + 6, base_x, "|")
        stdscr.addstr(base_y + 7, base_x, "|_____")
        
        # Body parts based on wrong count
        if wrong_count >= 1:  # Head
            stdscr.addstr(base_y + 4, base_x + 6, "O")
        if wrong_count >= 2:  # Body
            stdscr.addstr(base_y + 5, base_x + 6, "|")
        if wrong_count >= 3:  # Left arm
            stdscr.addstr(base_y + 5, base_x + 5, "/")
        if wrong_count >= 4:  # Right arm
            stdscr.addstr(base_y + 5, base_x + 7, "\\")
        if wrong_count >= 5:  # Left leg
            stdscr.addstr(base_y + 6, base_x + 5, "/")
        if wrong_count >= 6:  # Right leg
            stdscr.addstr(base_y + 6, base_x + 7, "\\")
