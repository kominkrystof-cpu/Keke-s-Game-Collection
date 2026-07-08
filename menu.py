"""Main menu system for Keke's Game Collection."""
import curses
from games import TicTacToe, GuessTheNumber, Hangman, RockPaperScissors, Blackjack, Wordle, DiceBet


class GameMenu:
    """Interactive menu for game selection."""
    
    def __init__(self):
        """Initialize the menu with available games."""
        self.games = [
            TicTacToe(),
            GuessTheNumber(),
            Hangman(),
            RockPaperScissors(),
            Blackjack(),
            Wordle(),
            DiceBet()
        ]
        self.selected_index = 0
    
    def run(self, stdscr):
        """Main menu loop."""
        # Initialize curses
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
        
        running = True
        
        while running:
            self.draw_menu(stdscr)
            
            # Handle input
            key = stdscr.getch()
            
            if key == curses.KEY_UP:
                self.selected_index = (self.selected_index - 1) % len(self.games)
            elif key == curses.KEY_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.games)
            elif key == curses.KEY_ENTER or key in [10, 13]:
                # Launch selected game
                self.games[self.selected_index].play(stdscr)
            elif key == ord('q'):
                running = False
    
    def draw_menu(self, stdscr):
        """Draw the menu interface with error handling for small terminals."""
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        
        # ASCII Art Header - Exact raw string for "Keke's Game Collection"
        header = r"""
  _  __    _        _        _____                         _____      _ _           _   _             
 | |/ /   | |      ( )      / ____|                       / ____|    | | |         | | (_)            
 | ' / ___| | _____|/ ___  | |  __  __ _ _ __ ___   ___  | |     ___ | | | ___  ___| |_ _  ___  _ __  
 |  < / _ \ |/ / _ \ / __| | | |_ |/ _` | '_ ` _ \ / _ \ | |    / _ \| | |/ _ \/ __| __| |/ _ \| '_ \ 
 | . \  __/   <  __/ \__ \ | |__| | (_| | | | | | |  __/ | |___| (_) | | |  __/ (__| |_| | (_) | | | |
 |_|\_\___|_|\_\___| |___/  \_____|\__,_|_| |_| |_|\___|  \_____\___/|_|_|\___|\___|\__|_|\___/|_| |_|
                                                                                                      
                                                                                                     
""".split('\n')
        
        # Draw header with error handling
        header_start_y = 2
        for i, line in enumerate(header):
            y = header_start_y + i
            x = (w - len(line)) // 2
            # Only draw if line fits within terminal width and height
            if y < h - 1 and len(line) <= w:
                try:
                    stdscr.addstr(y, x, line, curses.color_pair(1))
                except curses.error:
                    pass  # Skip this line if it doesn't fit
        
        # Draw separator with error handling
        separator = "=" * 50
        sep_y = header_start_y + len(header) + 1
        if sep_y < h - 1 and len(separator) <= w:
            try:
                stdscr.addstr(sep_y, (w - len(separator)) // 2, separator, curses.color_pair(2))
            except curses.error:
                pass
        
        # Draw game list with error handling
        menu_start_y = header_start_y + len(header) + 4
        for i, game in enumerate(self.games):
            if i == self.selected_index:
                prefix = "► "
                color = curses.color_pair(3) | curses.A_BOLD
            else:
                prefix = "  "
                color = curses.A_NORMAL
            
            game_line = f"{prefix}{game.name}"
            y = menu_start_y + i * 2
            x = (w - len(game_line)) // 2
            
            if y < h - 1 and len(game_line) <= w:
                try:
                    stdscr.addstr(y, x, game_line, color)
                except curses.error:
                    pass
        
        # Draw description area with error handling
        desc_start_y = menu_start_y + len(self.games) * 2 + 2
        selected_game = self.games[self.selected_index]
        desc_label = "Description:"
        desc_text = selected_game.description
        
        if desc_start_y < h - 2:
            try:
                stdscr.addstr(desc_start_y, (w - len(desc_label)) // 2, desc_label, curses.color_pair(2) | curses.A_BOLD)
            except curses.error:
                pass
        
        if desc_start_y + 1 < h - 1:
            try:
                stdscr.addstr(desc_start_y + 1, (w - len(desc_text)) // 2, desc_text, curses.A_DIM)
            except curses.error:
                pass
        
        # Draw footer instructions with error handling
        footer_y = h - 3
        instructions = [
            "Use UP/DOWN arrows to navigate",
            "Press ENTER to play a game",
            "Press Q to quit"
        ]
        
        for i, instruction in enumerate(instructions):
            y = footer_y + i
            if y < h - 1 and len(instruction) <= w:
                try:
                    stdscr.addstr(y, (w - len(instruction)) // 2, instruction, curses.color_pair(2))
                except curses.error:
                    pass
        
        stdscr.refresh()


def main(stdscr):
    """Entry point for curses application."""
    menu = GameMenu()
    menu.run(stdscr)


if __name__ == "__main__":
    curses.wrapper(main)
