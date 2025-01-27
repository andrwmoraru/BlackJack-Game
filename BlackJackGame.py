import random
import tkinter as tk
from tkinter import messagebox
import pyttsx3
 
# Constants for the cards
HEARTS = chr(9829)    # ♥
DIAMONDS = chr(9830)  # ♦
SPADES = chr(9824)    # ♠
CLUBS = chr(9827)     # ♣
BACKSIDE = 'backside'
 
 
class BlackjackGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")
        self.money = 5000
        self.bet = 0
        self.deck = []
        self.playerHand = []
        self.dealerHand = []
        self.engine = pyttsx3.init()
        self.init_gui()
 
    def init_gui(self):
        """Initialize the game interface."""
        self.info_label = tk.Label(self.root, text=f"Money: {self.money} | Bet: {self.bet}", font=("Arial", 14))
        self.info_label.pack(pady=10)
 
        self.dealer_frame = tk.LabelFrame(self.root, text="Dealer", font=("Arial", 12))
        self.dealer_frame.pack(pady=10)
        self.dealer_cards_label = tk.Label(self.dealer_frame, text="", font=("Courier", 12), justify="left")
        self.dealer_cards_label.pack()
 
        self.player_frame = tk.LabelFrame(self.root, text="Player", font=("Arial", 12))
        self.player_frame.pack(pady=10)
        self.player_cards_label = tk.Label(self.player_frame, text="", font=("Courier", 12), justify="left")
        self.player_cards_label.pack()
 
        self.hit_button = tk.Button(self.root, text="Hit", command=lambda: self.handle_move('H'))
        self.hit_button.pack(side=tk.LEFT, padx=10, pady=10)
 
        self.stand_button = tk.Button(self.root, text="Stand", command=lambda: self.handle_move('S'))
        self.stand_button.pack(side=tk.LEFT, padx=10, pady=10)
 
        self.double_button = tk.Button(self.root, text="Double", command=self.handle_double)
        self.double_button.pack(side=tk.LEFT, padx=10, pady=10)
 
        self.start_button = tk.Button(self.root, text="Start New Game", command=self.start_new_game)
        self.start_button.pack(pady=10)
 
    def update_display(self, reveal_dealer=False):
        """Update the game display with the current hands and info."""
        self.info_label.config(text=f"Money: {self.money} | Bet: {self.bet}")
        self.dealer_cards_label.config(text=self.get_hand_display(self.dealerHand, hidden=not reveal_dealer))
        self.player_cards_label.config(text=self.get_hand_display(self.playerHand))
        self.announce_player_hand_value()
 
    def start_new_game(self):
        """Start a new round."""
        if self.money <= 0:
            messagebox.showinfo("Game Over", "You're out of money! Game over!")
            self.root.quit()
            return
 
        self.bet = min(self.money, 100)
        self.deck = self.get_deck()
        self.playerHand = [self.deck.pop(), self.deck.pop()]
        self.dealerHand = [self.deck.pop(), self.deck.pop()]
        self.update_display()
 
    def handle_double(self):
        """Handle the 'Double' move."""
        if self.money >= self.bet * 2:
            self.money -= self.bet  # Deduct the additional bet
            self.bet *= 2  # Double the bet
            self.playerHand.append(self.deck.pop())  # Player takes one card
            self.update_display()
 
            # Check if the player busts after doubling
            if self.get_hand_value(self.playerHand) > 21:
                messagebox.showinfo("Game Over", "You busted after doubling! You lose!")
                self.money -= self.bet
                self.start_new_game()
                return
 
            # Player must stand after doubling
            self.handle_move('S')
        else:
            messagebox.showwarning("Insufficient Funds", "You don't have enough money to double the bet!")
 
    def handle_move(self, move):
        """Handle player moves."""
        if move == 'H':
            self.playerHand.append(self.deck.pop())
            if self.get_hand_value(self.playerHand) > 21:
                self.update_display()
                messagebox.showinfo("Game Over", "You busted! You lose!")
                self.money -= self.bet
                self.start_new_game()
                return
        elif move == 'S':
            while self.get_hand_value(self.dealerHand) < 17:
                self.dealerHand.append(self.deck.pop())
 
            self.update_display(reveal_dealer=True)
            self.check_game_status()
            return
 
        self.update_display()
 
    def check_game_status(self):
        """Check if the game has ended."""
        player_value = self.get_hand_value(self.playerHand)
        dealer_value = self.get_hand_value(self.dealerHand)
 
        if player_value > 21:
            messagebox.showinfo("Game Over", "You busted! You lose!")
            self.money -= self.bet
        elif dealer_value > 21 or player_value > dealer_value:
            messagebox.showinfo("Game Over", f"You win! You earned {self.bet}")
            self.money += self.bet
        elif player_value < dealer_value:
            messagebox.showinfo("Game Over", "You lose!")
            self.money -= self.bet
        else:
            messagebox.showinfo("Game Over", "It's a tie! Bet returned.")
 
        self.start_new_game()
 
    def get_deck(self):
        """Return a shuffled deck of cards."""
        deck = [(str(rank), suit) for suit in (HEARTS, DIAMONDS, SPADES, CLUBS) for rank in list(range(2, 11)) + ['J', 'Q', 'K', 'A']]
        random.shuffle(deck)
        return deck
 
    def get_hand_value(self, hand):
        """Calculate the value of a hand."""
        value = 0
        aces = 0
        for card in hand:
            rank = card[0]
            if rank in 'JQK':
                value += 10
            elif rank == 'A':
                aces += 1
                value += 1
            else:
                value += int(rank)
 
        for _ in range(aces):
            if value + 10 <= 21:
                value += 10
 
        return value
 
    def get_hand_display(self, hand, hidden=False):
        """Return a text representation of a hand with card graphics."""
        rows = ["", "", "", ""]
        if hidden:
            rows[0] += " ___  " + " ___  "
            rows[1] += "|## | " + f"|{hand[1][0].ljust(2)} | "
            rows[2] += "|###| " + f"| {hand[1][1]} | "
            rows[3] += "|_##| " + f"|_{hand[1][0].rjust(2, '_')}|"
        else:
            for card in hand:
                rank, suit = card
                rows[0] += " ___  "
                rows[1] += f"|{rank.ljust(2)} | "
                rows[2] += f"| {suit} | "
                rows[3] += f"|_{rank.rjust(2, '_')}| "
 
        return "\n".join(rows)
 
    def announce_player_hand_value(self):
        """Announce the player's hand value using text-to-speech."""
        hand_value = self.get_hand_value(self.playerHand)
        self.engine.say(f"{hand_value}")
        self.engine.runAndWait()
 
 
if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()