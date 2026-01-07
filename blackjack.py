import random
from enum import Enum

class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f"{self.rank}{self.suit.value}"
    
    def get_value(self):
        """Returns the value of the card for blackjack"""
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)

class Deck:
    def __init__(self, num_decks=1):
        self.cards = []
        self.num_decks = num_decks
        self.reset()
    
    def reset(self):
        """Create a fresh deck(s)"""
        self.cards = []
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for _ in range(self.num_decks):
            for suit in Suit:
                for rank in ranks:
                    self.cards.append(Card(suit, rank))
        random.shuffle(self.cards)
    
    def draw(self):
        """Draw a card from the deck"""
        if len(self.cards) < 10:
            self.reset()
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []
    
    def add_card(self, card):
        """Add a card to the hand"""
        self.cards.append(card)
    
    def get_value(self):
        """Calculate hand value, accounting for Aces"""
        value = 0
        aces = 0
        
        for card in self.cards:
            value += card.get_value()
            if card.rank == 'A':
                aces += 1
        
        # Adjust for Aces if hand is over 21
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        
        return value
    
    def is_blackjack(self):
        """Check if hand is a natural blackjack (21 with 2 cards)"""
        return len(self.cards) == 2 and self.get_value() == 21
    
    def __str__(self):
        return ", ".join(str(card) for card in self.cards)

class BlackjackGame:
    def __init__(self):
        self.deck = Deck(num_decks=6)
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.player_balance = 1000
        self.starting_balance = 1000
        self.current_bet = 0
        self.wins = 0
        self.losses = 0
        self.pushes = 0
        self.blackjacks = 0
        self.busts = 0
        self.total_wagered = 0
        self.total_won = 0
    
    def start_round(self):
        """Start a new round of blackjack"""
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        
        # Deal two cards to each
        self.player_hand.add_card(self.deck.draw())
        self.dealer_hand.add_card(self.deck.draw())
        self.player_hand.add_card(self.deck.draw())
        self.dealer_hand.add_card(self.deck.draw())
    
    def player_hit(self):
        """Player takes another card"""
        self.player_hand.add_card(self.deck.draw())
        return self.player_hand.get_value() <= 21
    
    def dealer_play(self):
        """Dealer plays according to standard rules (hit on 16 or less, stand on 17+)"""
        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_card(self.deck.draw())
    
    def determine_winner(self):
        """Determine the winner and return payout multiplier"""
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()
        
        # Player busted
        if player_value > 21:
            self.busts += 1
            self.losses += 1
            return -1, "Player busted! Dealer wins."
        
        # Dealer busted
        if dealer_value > 21:
            self.wins += 1
            return 2, "Dealer busted! Player wins!"
        
        # Check for blackjack
        if self.player_hand.is_blackjack() and not self.dealer_hand.is_blackjack():
            self.wins += 1
            self.blackjacks += 1
            return 2.5, "Blackjack! Player wins!"
        
        if self.dealer_hand.is_blackjack() and not self.player_hand.is_blackjack():
            self.losses += 1
            return -1, "Dealer has blackjack. Dealer wins."
        
        if self.player_hand.is_blackjack() and self.dealer_hand.is_blackjack():
            self.pushes += 1
            return 1, "Both have blackjack. Push!"
        
        # Compare values
        if player_value > dealer_value:
            self.wins += 1
            return 2, "Player wins!"
        elif dealer_value > player_value:
            self.losses += 1
            return -1, "Dealer wins."
        else:
            self.pushes += 1
            return 1, "Push! It's a tie."
    
    def display_state(self, show_dealer_hole=False):
        """Display current game state"""
        print("\n" + "="*50)
        print(f"DEALER'S HAND: {self.dealer_hand}", end="")
        if show_dealer_hole:
            print(f" → Value: {self.dealer_hand.get_value()}")
        else:
            print(" (one card hidden)")
        
        print(f"YOUR HAND:    {self.player_hand} → Value: {self.player_hand.get_value()}")
        print("="*50)
        print(f"Balance: ${self.player_balance} | Bet: ${self.current_bet}")
    
    def display_statistics(self):
        """Display comprehensive statistical analysis"""
        total_rounds = self.wins + self.losses + self.pushes
        
        if total_rounds == 0:
            print("No hands played.")
            return
        
        # Calculate percentages
        win_percentage = (self.wins / total_rounds) * 100
        loss_percentage = (self.losses / total_rounds) * 100
        push_percentage = (self.pushes / total_rounds) * 100
        blackjack_percentage = (self.blackjacks / total_rounds) * 100
        bust_percentage = (self.busts / total_rounds) * 100
        
        # Calculate profit/loss
        profit_loss = self.player_balance - self.starting_balance
        roi = (profit_loss / self.starting_balance) * 100
        
        # Calculate average bet and payout
        average_bet = self.total_wagered / total_rounds if total_rounds > 0 else 0
        average_win = self.total_won / self.wins if self.wins > 0 else 0
        
        # Display results
        print("\n" + "="*60)
        print(" " * 15 + "📊 GAME STATISTICS & ANALYSIS")
        print("="*60)
        
        print("\n💰 FINANCIAL SUMMARY:")
        print(f"  Starting Balance:    ${self.starting_balance:,}")
        print(f"  Final Balance:       ${self.player_balance:,}")
        print(f"  Total Wagered:       ${self.total_wagered:,}")
        if profit_loss >= 0:
            print(f"  Net Profit:          🟢 +${profit_loss:,}")
            print(f"  Return on Investment: 🟢 +{roi:.2f}%")
        else:
            print(f"  Net Loss:            🔴 ${profit_loss:,}")
            print(f"  Return on Investment: 🔴 {roi:.2f}%")
        
        print("\n🎮 GAMEPLAY STATISTICS:")
        print(f"  Total Hands Played:  {total_rounds}")
        print(f"  Wins:                {self.wins} ({win_percentage:.1f}%)")
        print(f"  Losses:              {self.losses} ({loss_percentage:.1f}%)")
        print(f"  Pushes (Ties):       {self.pushes} ({push_percentage:.1f}%)")
        
        print("\n⭐ SPECIAL EVENTS:")
        print(f"  Blackjacks:          {self.blackjacks} ({blackjack_percentage:.1f}% of hands)")
        print(f"  Busts:               {self.busts} ({bust_percentage:.1f}% of losses)")
        
        print("\n📈 BETTING ANALYSIS:")
        print(f"  Average Bet:         ${average_bet:.2f}")
        print(f"  Average Win Payout:  ${average_win:.2f}")
        print(f"  Win/Loss Ratio:      {self.wins}:{self.losses}")
        
        # House edge estimation
        if total_rounds >= 10:
            house_edge = (abs(profit_loss) / self.total_wagered * 100) if self.total_wagered > 0 else 0
            print(f"  Effective House Edge: {house_edge:.2f}%")
        
        print("\n" + "="*60)
        
        # Performance evaluation
        print("\n🎯 PERFORMANCE EVALUATION:")
        if win_percentage >= 60:
            print("  ⭐⭐⭐ Exceptional! You beat the house!")
        elif win_percentage >= 50:
            print("  ⭐⭐ Great performance! Close to break-even.")
        elif win_percentage >= 45:
            print("  ⭐ Good effort! You're near average.")
        else:
            print("  💡 The house always wins. Better luck next time!")
        
        print("="*60 + "\n")
    
    def play(self):
        """Main game loop"""
        print("\n" + "="*50)
        print("          ♠ BLACKJACK ♠")
        print("="*50)
        
        while self.player_balance > 0:
            # Get bet
            while True:
                try:
                    print(f"\n💰 Balance: ${self.player_balance}")
                    bet = int(input("Place your bet: $"))
                    if bet <= 0 or bet > self.player_balance:
                        print("❌ Invalid bet. Try again.")
                        continue
                    self.current_bet = bet
                    self.total_wagered += bet
                    self.player_balance -= bet
                    break
                except ValueError:
                    print("❌ Please enter a valid number.")
            
            # Start round
            self.start_round()
            self.display_state()
            
            # Check for dealer blackjack
            if self.dealer_hand.is_blackjack():
                self.display_state(show_dealer_hole=True)
                if self.player_hand.is_blackjack():
                    print("✓ Both have blackjack. Push!")
                    self.pushes += 1
                    self.player_balance += self.current_bet
                else:
                    print("✗ Dealer has blackjack. You lose.")
                    self.losses += 1
                continue
            
            # Check for player blackjack
            if self.player_hand.is_blackjack():
                self.display_state(show_dealer_hole=True)
                win_amount = int(self.current_bet * 2.5)
                print(f"✓ BLACKJACK! You win ${win_amount}!")
                self.wins += 1
                self.blackjacks += 1
                self.total_won += win_amount
                self.player_balance += win_amount
                continue
            
            # Player's turn
            bust = False
            doubled = False
            while True:
                if len(self.player_hand.cards) == 2 and not doubled:
                    action = input("\n(H)it, (S)tand, or (D)ouble Down? ").lower()
                else:
                    action = input("\n(H)it or (S)tand? ").lower()
                
                if action == 'h':
                    if not self.player_hit():
                        self.display_state(show_dealer_hole=True)
                        print("✗ You busted! You lose.")
                        bust = True
                        break
                    self.display_state()
                elif action == 's':
                    break
                elif action == 'd' and len(self.player_hand.cards) == 2 and not doubled:
                    # Double down
                    if self.current_bet > self.player_balance:
                        print("❌ Not enough balance to double down.")
                        continue
                    self.player_balance -= self.current_bet
                    self.current_bet *= 2
                    self.total_wagered += self.current_bet // 2
                    doubled = True
                    print(f"✓ Doubled down! New bet: ${self.current_bet}")
                    if not self.player_hit():
                        self.display_state(show_dealer_hole=True)
                        print("✗ You busted! You lose.")
                        bust = True
                        break
                    self.display_state()
                    break
                else:
                    print("❌ Enter 'h', 's', or 'd'.")
            
            if not bust:
                # Player stands, dealer plays
                self.dealer_play()
                self.display_state(show_dealer_hole=True)
                multiplier, result = self.determine_winner()
                print(f"✓ {result}")
                payout = int(self.current_bet * multiplier)
                self.player_balance += payout
                if multiplier > 0:
                    self.total_won += payout
            
            # Ask to play again
            if self.player_balance <= 0:
                print("\n✗ Game Over! You're out of chips.")
                self.display_statistics()
            else:
                play_again = input("\nPlay another round? (y/n) ").lower()
                if play_again != 'y':
                    self.display_statistics()
                    break
        
        print("Thanks for playing!")

if __name__ == "__main__":
    game = BlackjackGame()
    game.play()
