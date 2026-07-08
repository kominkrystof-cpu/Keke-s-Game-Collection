"""Guess the Number game implementation."""
import curses
import random
from .base import Game


class GuessTheNumber(Game):
    """Guess the Number game."""
    
    @property
    def name(self) -> str:
        return "Guess the Number"
    
    @property
    def description(self) -> str:
        return "Guess a number between 1 and 100"
    
    def play(self, stdscr):
        """Main game loop for Guess the Number."""
        curses.curs_set(1)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        
        h, w = stdscr.getmaxyx()
        
        secret = random.randint(1, 100)
        attempts = 0
        guess = ""
        message = "Enter your guess (1-100): "
        feedback = ""
        game_over = False
        
        # Witty responses
        too_low_responses = [
            "Too low! Aim for the stars, buddy!",
            "Not even close! Did you leave your brain in the other room?",
            "Too low! My grandma guesses higher than that!",
            "Way too low! Try again, you can do better!",
            "Too low! The number is laughing at you right now.",
            "Too low! Dig deeper!",
            "Too low! You're barely scratching the surface!"
        ]
        
        too_high_responses = [
            "A bit too high, calm down!",
            "Too high! You're overshooting like a rocket!",
            "Way too high! Bring it down a notch!",
            "Too high! The number is scared of you!",
            "Too high! You're reaching for the moon!",
            "Too high! Lower your expectations!",
            "Too high! Chill out and guess lower!"
        ]
        
        while not game_over:
            stdscr.clear()
            
            # Title
            title = "GUESS THE NUMBER"
            stdscr.addstr(2, (w - len(title)) // 2, title, curses.A_BOLD | curses.color_pair(1))
            
            # Draw box border around input area
            box_y = 4
            box_x = (w - 30) // 2
            box_width = 30
            box_height = 7
            
            # Draw box
            stdscr.addstr(box_y, box_x, "┌" + "─" * (box_width - 2) + "┐", curses.color_pair(2))
            for i in range(1, box_height - 1):
                stdscr.addstr(box_y + i, box_x, "│", curses.color_pair(2))
                stdscr.addstr(box_y + i, box_x + box_width - 1, "│", curses.color_pair(2))
            stdscr.addstr(box_y + box_height - 1, box_x, "└" + "─" * (box_width - 2) + "┘", curses.color_pair(2))
            
            # Instructions inside box
            stdscr.addstr(box_y + 1, box_x + 2, message, curses.A_NORMAL)
            
            # Current guess inside box
            stdscr.addstr(box_y + 2, box_x + 2, "Guess: " + guess + "_", curses.color_pair(5) | curses.A_BOLD)
            
            # Feedback
            if feedback:
                if "correct" in feedback.lower():
                    color = curses.color_pair(3) | curses.A_BOLD
                elif "low" in feedback.lower():
                    color = curses.color_pair(4) | curses.A_BOLD
                elif "high" in feedback.lower():
                    color = curses.color_pair(4) | curses.A_BOLD
                else:
                    color = curses.color_pair(2)
                stdscr.addstr(box_y + 4, box_x + 2, feedback, color)
            
            # Attempts
            stdscr.addstr(box_y + 6, box_x + 2, f"Attempts: {attempts}", curses.color_pair(1) | curses.A_BOLD)
            
            # Help
            help_text = "ENTER to submit | Q to quit"
            stdscr.addstr(h - 2, (w - len(help_text)) // 2, help_text, curses.A_DIM)
            
            stdscr.refresh()
            
            # Handle input
            key = stdscr.getch()
            
            if key == curses.KEY_ENTER or key in [10, 13]:
                if guess:
                    try:
                        num = int(guess)
                        attempts += 1
                        
                        if num == secret:
                            feedback = f"Correct! You got it in {attempts} attempts!"
                            game_over = True
                        elif num < secret:
                            feedback = random.choice(too_low_responses)
                        else:
                            feedback = random.choice(too_high_responses)
                        
                        guess = ""
                    except ValueError:
                        feedback = "Please enter a valid number!"
            elif key == curses.KEY_BACKSPACE or key == 127:
                guess = guess[:-1]
            elif key == ord('q'):
                break
            elif 48 <= key <= 57:  # Digits 0-9
                if len(guess) < 3:
                    guess += chr(key)
            
            if game_over:
                # Game over loop - wait for Q to quit
                while True:
                    key = stdscr.getch()
                    if key == ord('q'):
                        break
                break
