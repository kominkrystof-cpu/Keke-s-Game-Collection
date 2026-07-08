"""Rock Paper Scissors game implementation."""
import curses
import random
from .base import Game


class RockPaperScissors(Game):
    """Rock Paper Scissors game against a bot."""
    
    @property
    def name(self) -> str:
        return "Rock Paper Scissors"
    
    @property
    def description(self) -> str:
        return "Classic hand game against the computer"
    
    def play(self, stdscr):
        """Main game loop for Rock Paper Scissors."""
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE)
        
        h, w = stdscr.getmaxyx()
        
        choices = ['Rock', 'Paper', 'Scissors']
        player_choice = 0  # 0=Rock, 1=Paper, 2=Scissors
        game_over = False
        result = None
        computer_choice = None
        
        while not game_over:
            self.draw_game(stdscr, player_choice, result, computer_choice, h, w)
            
            if game_over:
                # Game over loop - wait for Q to quit
                while True:
                    key = stdscr.getch()
                    if key == ord('q'):
                        break
                break
            
            # Handle input
            key = stdscr.getch()
            
            if key == curses.KEY_LEFT:
                player_choice = (player_choice - 1) % 3
            elif key == curses.KEY_RIGHT:
                player_choice = (player_choice + 1) % 3
            elif key == curses.KEY_ENTER or key in [10, 13]:
                # Play round
                computer_choice = random.randint(0, 2)
                result = self.determine_winner(player_choice, computer_choice)
                game_over = True
            elif key == ord('q'):
                break
    
    def draw_game(self, stdscr, player_choice, result, computer_choice, h, w):
        """Draw the game interface."""
        stdscr.clear()
        
        # Title
        title = "ROCK PAPER SCISSORS"
        stdscr.addstr(2, (w - len(title)) // 2, title, curses.A_BOLD | curses.color_pair(1))
        
        choices = ['Rock', 'Paper', 'Scissors']
        
        # Draw player choices
        stdscr.addstr(6, (w - 20) // 2, "Your Choice:", curses.color_pair(2) | curses.A_BOLD)
        
        for i, choice in enumerate(choices):
            prefix = "► " if i == player_choice and not result else "  "
            color = curses.color_pair(5) | curses.A_BOLD if i == player_choice and not result else curses.A_NORMAL
            stdscr.addstr(8 + i, (w - 20) // 2, f"{prefix}{choice}", color)
        
        # Result display
        if result is not None:
            result_y = 14
            if result == 'win':
                msg = "YOU WON! Press 'Q' to return to menu"
                color = curses.color_pair(3) | curses.A_BOLD
            elif result == 'lose':
                msg = "YOU FAILED! Press 'Q' to return to menu"
                color = curses.color_pair(4) | curses.A_BOLD
            else:
                msg = "IT'S A DRAW! Press 'Q' to return to menu"
                color = curses.color_pair(2) | curses.A_BOLD
            
            stdscr.addstr(result_y, (w - len(msg)) // 2, msg, color)
            
            # Show what each chose
            if computer_choice is not None:
                stdscr.addstr(result_y + 2, (w - 30) // 2, f"You chose: {choices[player_choice]}", curses.color_pair(2))
                stdscr.addstr(result_y + 3, (w - 30) // 2, f"Computer chose: {choices[computer_choice]}", curses.color_pair(2))
        else:
            stdscr.addstr(14, (w - 30) // 2, "Use LEFT/RIGHT to select, ENTER to play", curses.color_pair(2))
        
        # Footer
        footer = "Press Q to quit to menu"
        stdscr.addstr(h - 2, (w - len(footer)) // 2, footer, curses.A_DIM)
        
        stdscr.refresh()
    
    def determine_winner(self, player, computer):
        """Determine the winner of a round."""
        if player == computer:
            return 'draw'
        # Rock beats Scissors, Scissors beats Paper, Paper beats Rock
        if (player == 0 and computer == 2) or (player == 2 and computer == 1) or (player == 1 and computer == 0):
            return 'win'
        return 'lose'
