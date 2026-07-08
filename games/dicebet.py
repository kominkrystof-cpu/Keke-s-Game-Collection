"""Dice Bet game implementation."""
import curses
import random
from .base import Game


class DiceBet(Game):
    """Higher/Lower dice rolling game with streak system."""
    
    @property
    def name(self) -> str:
        return "Dice Bet"
    
    @property
    def description(self) -> str:
        return "Guess if the next roll will be higher or lower"
    
    def play(self, stdscr):
        """Main game loop for Dice Bet."""
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE)
        
        h, w = stdscr.getmaxyx()
        
        current_roll = random.randint(1, 6)
        streak = 0
        best_streak = 0
        game_over = False
        result = None
        next_roll = None
        
        while not game_over:
            self.draw_game(stdscr, current_roll, streak, best_streak, result, next_roll, h, w)
            
            if game_over:
                # Game over loop - wait for Q to quit
                while True:
                    key = stdscr.getch()
                    if key == ord('q'):
                        break
                break
            
            # Handle input
            key = stdscr.getch()
            
            if key == curses.KEY_UP:
                # Bet higher
                next_roll = random.randint(1, 6)
                if next_roll > current_roll:
                    streak += 1
                    if streak > best_streak:
                        best_streak = streak
                    result = 'win'
                elif next_roll < current_roll:
                    streak = 0
                    result = 'lose'
                    game_over = True
                else:
                    result = 'tie'
                current_roll = next_roll
            elif key == curses.KEY_DOWN:
                # Bet lower
                next_roll = random.randint(1, 6)
                if next_roll < current_roll:
                    streak += 1
                    if streak > best_streak:
                        best_streak = streak
                    result = 'win'
                elif next_roll > current_roll:
                    streak = 0
                    result = 'lose'
                    game_over = True
                else:
                    result = 'tie'
                current_roll = next_roll
            elif key == ord('q'):
                break
    
    def draw_game(self, stdscr, current_roll, streak, best_streak, result, next_roll, h, w):
        """Draw the game interface."""
        stdscr.clear()
        
        # Title
        title = "DICE BET"
        stdscr.addstr(2, (w - len(title)) // 2, title, curses.A_BOLD | curses.color_pair(1))
        
        # Draw current dice
        dice_y = 6
        dice_x = (w - 7) // 2
        stdscr.addstr(dice_y, dice_x, "┌─────┐", curses.color_pair(2))
        stdscr.addstr(dice_y + 1, dice_x, "│     │", curses.color_pair(2))
        
        # Draw dice face
        face = self.get_dice_face(current_roll)
        stdscr.addstr(dice_y + 2, dice_x, f"│ {face} │", curses.color_pair(5) | curses.A_BOLD)
        
        stdscr.addstr(dice_y + 3, dice_x, "│     │", curses.color_pair(2))
        stdscr.addstr(dice_y + 4, dice_x, "└─────┘", curses.color_pair(2))
        
        # Show roll number
        stdscr.addstr(dice_y + 5, (w - 15) // 2, f"Current Roll: {current_roll}", curses.color_pair(2))
        
        # Show streak
        stdscr.addstr(dice_y + 7, (w - 20) // 2, f"Current Streak: {streak}", curses.color_pair(3) | curses.A_BOLD)
        stdscr.addstr(dice_y + 8, (w - 20) // 2, f"Best Streak: {best_streak}", curses.color_pair(1) | curses.A_BOLD)
        
        # Result display
        if result is not None:
            result_y = dice_y + 10
            if result == 'win':
                msg = "Correct! Keep going!"
                color = curses.color_pair(3) | curses.A_BOLD
            elif result == 'lose':
                msg = "Wrong! Game Over!"
                color = curses.color_pair(4) | curses.A_BOLD
            else:
                msg = "Tie! Try again!"
                color = curses.color_pair(2) | curses.A_BOLD
            
            stdscr.addstr(result_y, (w - len(msg)) // 2, msg, color)
            
            if next_roll is not None:
                roll_msg = f"Next roll was: {next_roll}"
                stdscr.addstr(result_y + 1, (w - len(roll_msg)) // 2, roll_msg, curses.color_pair(2))
        
        if result == 'lose':
            game_over_msg = "YOU FAILED! Press 'Q' to return to menu"
            stdscr.addstr(result_y + 3, (w - len(game_over_msg)) // 2, game_over_msg, curses.color_pair(4) | curses.A_BOLD)
        else:
            stdscr.addstr(dice_y + 12, (w - 35) // 2, "UP: Bet Higher | DOWN: Bet Lower", curses.color_pair(2))
        
        # Footer
        footer = "Press Q to quit to menu"
        stdscr.addstr(h - 2, (w - len(footer)) // 2, footer, curses.A_DIM)
        
        stdscr.refresh()
    
    def get_dice_face(self, number):
        """Get the ASCII representation of a dice face."""
        faces = {
            1: "  ●  ",
            2: "●   ●",
            3: "● ● ●",
            4: "● ● ●",
            5: "●●●●●",
            6: "●●●●●"
        }
        return faces.get(number, "     ")
