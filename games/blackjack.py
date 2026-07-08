"""Blackjack game implementation."""
import curses
import random
from .base import Game


class Blackjack(Game):
    """Simplified Blackjack game against a dealer."""
    
    @property
    def name(self) -> str:
        return "Blackjack"
    
    @property
    def description(self) -> str:
        return "Classic 21 card game against the dealer"
    
    def play(self, stdscr):
        """Main game loop for Blackjack."""
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE)
        
        h, w = stdscr.getmaxyx()
        
        suits = ['♥', '♦', '♣', '♠']
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        
        player_hand = []
        dealer_hand = []
        game_over = False
        result = None
        player_turn = True
        
        # Initial deal
        self.deal_card(player_hand, suits, values)
        self.deal_card(dealer_hand, suits, values)
        self.deal_card(player_hand, suits, values)
        self.deal_card(dealer_hand, suits, values)
        
        while not game_over:
            self.draw_game(stdscr, player_hand, dealer_hand, result, player_turn, h, w)
            
            if game_over:
                # Game over loop - wait for Q to quit
                while True:
                    key = stdscr.getch()
                    if key == ord('q'):
                        break
                break
            
            if player_turn:
                # Handle input
                key = stdscr.getch()
                
                if key == curses.KEY_ENTER or key in [10, 13]:
                    # Hit
                    self.deal_card(player_hand, suits, values)
                    if self.calculate_score(player_hand) > 21:
                        result = 'bust'
                        game_over = True
                elif key == ord('s'):
                    # Stand
                    player_turn = False
                    # Dealer plays
                    while self.calculate_score(dealer_hand) < 17:
                        self.deal_card(dealer_hand, suits, values)
                    
                    player_score = self.calculate_score(player_hand)
                    dealer_score = self.calculate_score(dealer_hand)
                    
                    if dealer_score > 21:
                        result = 'win'
                    elif dealer_score > player_score:
                        result = 'lose'
                    elif dealer_score < player_score:
                        result = 'win'
                    else:
                        result = 'draw'
                    game_over = True
                elif key == ord('q'):
                    break
            else:
                # Should not reach here
                break
    
    def deal_card(self, hand, suits, values):
        """Deal a random card to the hand."""
        suit = random.choice(suits)
        value = random.choice(values)
        hand.append((suit, value))
    
    def calculate_score(self, hand):
        """Calculate the score of a hand."""
        score = 0
        aces = 0
        
        for suit, value in hand:
            if value in ['J', 'Q', 'K']:
                score += 10
            elif value == 'A':
                aces += 1
                score += 11
            else:
                score += int(value)
        
        # Adjust for aces
        while score > 21 and aces > 0:
            score -= 10
            aces -= 1
        
        return score
    
    def draw_game(self, stdscr, player_hand, dealer_hand, result, player_turn, h, w):
        """Draw the game interface."""
        stdscr.clear()
        
        # Title
        title = "BLACKJACK"
        stdscr.addstr(2, (w - len(title)) // 2, title, curses.A_BOLD | curses.color_pair(1))
        
        # Draw dealer's hand
        stdscr.addstr(6, (w - 20) // 2, "Dealer's Hand:", curses.color_pair(2) | curses.A_BOLD)
        dealer_y = 8
        for i, (suit, value) in enumerate(dealer_hand):
            if i == 0 and player_turn:
                # Hide first card
                card_str = "??"
            else:
                card_str = f"{value}{suit}"
            stdscr.addstr(dealer_y + i, (w - 10) // 2, card_str, curses.color_pair(5))
        
        if not player_turn:
            dealer_score = self.calculate_score(dealer_hand)
            stdscr.addstr(dealer_y + len(dealer_hand) + 1, (w - 15) // 2, f"Score: {dealer_score}", curses.color_pair(2))
        
        # Draw player's hand
        stdscr.addstr(14, (w - 20) // 2, "Your Hand:", curses.color_pair(2) | curses.A_BOLD)
        player_y = 16
        for i, (suit, value) in enumerate(player_hand):
            card_str = f"{value}{suit}"
            stdscr.addstr(player_y + i, (w - 10) // 2, card_str, curses.color_pair(5))
        
        player_score = self.calculate_score(player_hand)
        stdscr.addstr(player_y + len(player_hand) + 1, (w - 15) // 2, f"Score: {player_score}", curses.color_pair(2))
        
        # Result display
        if result is not None:
            result_y = player_y + len(player_hand) + 3
            if result == 'win':
                msg = "YOU WON! Press 'Q' to return to menu"
                color = curses.color_pair(3) | curses.A_BOLD
            elif result == 'lose' or result == 'bust':
                msg = "YOU FAILED! Press 'Q' to return to menu"
                color = curses.color_pair(4) | curses.A_BOLD
            else:
                msg = "IT'S A DRAW! Press 'Q' to return to menu"
                color = curses.color_pair(2) | curses.A_BOLD
            
            stdscr.addstr(result_y, (w - len(msg)) // 2, msg, color)
        elif player_turn:
            stdscr.addstr(player_y + len(player_hand) + 3, (w - 30) // 2, "ENTER: Hit | S: Stand", curses.color_pair(2))
        
        # Footer
        footer = "Press Q to quit to menu"
        stdscr.addstr(h - 2, (w - len(footer)) // 2, footer, curses.A_DIM)
        
        stdscr.refresh()
