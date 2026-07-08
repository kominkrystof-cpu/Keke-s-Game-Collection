"""Tic Tac Toe game implementation."""
import curses
import random
import time
from .base import Game


class TicTacToe(Game):
    """Classic Tic Tac Toe game with AI opponent."""
    
    @property
    def name(self) -> str:
        return "Tic Tac Toe"
    
    @property
    def description(self) -> str:
        return "Play against the computer (You: X, AI: O)"
    
    def play(self, stdscr):
        """Main game loop for Tic Tac Toe."""
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
        
        h, w = stdscr.getmaxyx()
        
        board = [[' ' for _ in range(3)] for _ in range(3)]
        cursor_row, cursor_col = 1, 1  # Start in center
        game_over = False
        winner = None
        player_turn = True  # True = player (X), False = AI (O)
        
        while not game_over:
            self.draw_board(stdscr, board, cursor_row, cursor_col, winner, player_turn, h, w)
            
            if game_over:
                # Game over loop - wait for Q to quit
                while True:
                    key = stdscr.getch()
                    if key == ord('q'):
                        break
                break
            
            if player_turn:
                # Player's turn - handle input
                key = stdscr.getch()
                
                if key == curses.KEY_UP:
                    cursor_row = max(0, cursor_row - 1)
                elif key == curses.KEY_DOWN:
                    cursor_row = min(2, cursor_row + 1)
                elif key == curses.KEY_LEFT:
                    cursor_col = max(0, cursor_col - 1)
                elif key == curses.KEY_RIGHT:
                    cursor_col = min(2, cursor_col + 1)
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    # Place X if cell is empty
                    if board[cursor_row][cursor_col] == ' ':
                        board[cursor_row][cursor_col] = 'X'
                        winner = self.check_winner(board)
                        
                        if winner:
                            game_over = True
                        elif all(cell != ' ' for row in board for cell in row):
                            winner = 'Draw'
                            game_over = True
                        else:
                            player_turn = False
                elif key == ord('q'):
                    break
            else:
                # AI's turn
                stdscr.nodelay(False)
                curses.napms(500)  # Brief pause for realism
                
                # AI makes a move
                ai_row, ai_col = self.get_ai_move(board)
                if ai_row is not None:
                    board[ai_row][ai_col] = 'O'
                    winner = self.check_winner(board)
                    
                    if winner:
                        game_over = True
                    elif all(cell != ' ' for row in board for cell in row):
                        winner = 'Draw'
                        game_over = True
                    else:
                        player_turn = True
    
    def draw_board(self, stdscr, board, cursor_row, cursor_col, winner, player_turn, h, w):
        """Draw the game board with cursor highlighting and box borders."""
        stdscr.clear()
        
        # Title
        title = "TIC TAC TOE"
        stdscr.addstr(2, (w - len(title)) // 2, title, curses.A_BOLD | curses.color_pair(1))
        
        # Instructions
        if winner:
            if winner == 'Draw':
                msg = "GAME OVER - It's a draw! Press 'Q' to return to menu"
                color = curses.color_pair(2)
            elif winner == 'X':
                msg = "GAME OVER - You win! Press 'Q' to return to menu"
                color = curses.color_pair(4)
            else:
                msg = "GAME OVER - Computer wins! Press 'Q' to return to menu"
                color = curses.color_pair(5)
        elif player_turn:
            msg = "Your turn (X). Use arrow keys to move, ENTER to place"
            color = curses.color_pair(2)
        else:
            msg = "Computer is thinking..."
            color = curses.color_pair(2)
        stdscr.addstr(4, (w - len(msg)) // 2, msg, color | curses.A_BOLD)
        
        # Draw board with box border
        board_start_y = 6
        board_start_x = (w - 13) // 2
        
        # Draw top border
        stdscr.addstr(board_start_y, board_start_x, "┌───┬───┬───┐", curses.color_pair(1))
        
        for i in range(3):
            y = board_start_y + i * 2 + 1
            stdscr.addstr(y, board_start_x, "│", curses.color_pair(1))
            
            for j in range(3):
                cell = board[i][j]
                x = board_start_x + j * 4 + 1
                
                # Highlight cursor position
                if i == cursor_row and j == cursor_col and player_turn and not winner:
                    stdscr.addstr(y, x, f"[{cell}]", curses.color_pair(3) | curses.A_BOLD)
                else:
                    # Color X and O differently
                    if cell == 'X':
                        stdscr.addstr(y, x, f" {cell} ", curses.color_pair(4) | curses.A_BOLD)
                    elif cell == 'O':
                        stdscr.addstr(y, x, f" {cell} ", curses.color_pair(5) | curses.A_BOLD)
                    else:
                        stdscr.addstr(y, x, f" {cell} ")
                
                stdscr.addstr(y, x + 3, "│", curses.color_pair(1))
            
            # Draw separator between rows
            if i < 2:
                stdscr.addstr(y + 1, board_start_x, "├───┼───┼───┤", curses.color_pair(1))
        
        # Draw bottom border
        stdscr.addstr(board_start_y + 7, board_start_x, "└───┴───┴───┘", curses.color_pair(1))
        
        # Footer
        footer = "Press Q to quit to menu"
        stdscr.addstr(h - 2, (w - len(footer)) // 2, footer, curses.A_DIM)
        
        stdscr.refresh()
    
    def get_ai_move(self, board):
        """Get AI move - simple strategy: win if possible, block if needed, otherwise random."""
        empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
        
        if not empty_cells:
            return None, None
        
        # Try to win
        for row, col in empty_cells:
            board[row][col] = 'O'
            if self.check_winner(board) == 'O':
                board[row][col] = ' '
                return row, col
            board[row][col] = ' '
        
        # Block player from winning
        for row, col in empty_cells:
            board[row][col] = 'X'
            if self.check_winner(board) == 'X':
                board[row][col] = ' '
                return row, col
            board[row][col] = ' '
        
        # Take center if available
        if board[1][1] == ' ':
            return 1, 1
        
        # Random move
        return random.choice(empty_cells)
    
    def check_winner(self, board):
        """Check if there's a winner."""
        # Check rows
        for row in board:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]
        
        # Check columns
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] != ' ':
                return board[0][col]
        
        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] != ' ':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != ' ':
            return board[0][2]
        
        return None
