import random
import time

# const
MAX_PLAYERS = 5
DEFAULT_MONEY = 100

class BlackjackTable:
    def __init__(self):
        self.players = {}               # players in the game
        self.deck = Deck()              # deck of cards
        self.deck.shuffle_deck()
        self.current_turn_idx = None    # who's turn is it
        self.dealer = Dealer()          # dealer's set of cards
        self.scene = 0                  # current scene

    def get_id(self):
        """Finds an unassigned ID for new player

        Returns:
            int: ID of the new player or -1 if the table is full
        """
        for i in range(MAX_PLAYERS):
            if str(i) not in self.players.keys():
                return i
        return -1

    def join(self, player):
        """Allows a player to join the table

        Args:
            player (Player): Player that joined the table

        Returns:
            tuple: (err_code, player_id)
        """
        id = self.get_id()
        if id == -1:
            return -1, -1
        while self.scene != 0:
            time.sleep(2)
        self.players[str(id)] = player
        return 0, id

    def disconnect(self, player):
        """Disconnects the player from the game

        Args:
            player (int): player ID
        """
        self.does_player_exists(player)
        del self.players[str(player)]
        self.reset_ready()

    def is_all_player_ready(self):
        """Check if all the players are ready

        Returns:
            bool: if all the players are ready
        """
        for key in self.players.keys():
            if not self.players[key].is_ready:
                return False
        return True

    def reset_ready(self):
        """Reset the ready status
        """
        for key in self.players.keys():
            self.players[key].is_ready = False

    def reset_busted(self):
        """Reset the busted status
        """
        for key in self.players.keys():
            self.players[key].has_busted = False

    def reset_has_won(self):
        """Reset the busted status
        """
        for key in self.players.keys():
            self.players[key].has_won = None

    def player_ready(self, player):
        """Sets the player status to ready when in lobby

        Args:
            player (int): player ID
        """
        self.does_player_exists(player)
        if self.players[str(player)].is_ready:
            return
        self.players[str(player)].is_ready = True

        if self.is_all_player_ready():
            self.scene = 1
            self.reset_ready()

    def add_bet(self, id):
        self.does_player_exists(id)
        player = self.players[str(id)]
        if player.money > 0 and not player.is_ready:
            player.bet += 1
            player.money -= 1

    def sub_bet(self, id):
        self.does_player_exists(id)
        player = self.players[str(id)]
        if player.bet > 0 and not player.is_ready:
            player.bet -= 1
            player.money += 1

    def confirm_bet(self, id):
        self.does_player_exists(id)
        player = self.players[str(id)]
        if player.is_ready or player.bet == 0:
            return
        player.is_ready = True

        # transition
        if self.is_all_player_ready():
            self.scene = 2
            self.reset_ready()
            self.deal_cards_init()
            self.next_turn()

    def next_turn(self):
        if self.current_turn_idx is None:
            self.current_turn_idx = 0
        else:
            self.current_turn_idx += 1

        # if next player is nobody, it's dealer's turn
        if self.current_turn_idx >= len(self.players):
            self.scene += 1
            self.dealers_turn()
            return

        # keep iterating through until it goes through all player or player hasn't won
        keys = list(self.players.keys())
        curr_turn = keys[self.current_turn_idx]
        curr_player = self.players[curr_turn]
        
        while curr_player.has_won == 2:
            self.current_turn_idx += 1
            if self.current_turn_idx >= len(self.players):
                break
            curr_turn = keys[self.current_turn_idx]
            curr_player = self.players[curr_turn]

        if self.current_turn_idx >= len(self.players):
            self.scene += 1
            self.dealers_turn()
    
    def deal_cards_init(self):
        """Give dealer and all players 2 cards
        """
        self.deck.shuffle_deck()

        # Dealer gets 2 cards and see if blackjack occured
        self.dealer.get_cards(self.deck.draw_card())
        self.dealer.get_cards(self.deck.draw_card())
        self.dealer.cards[1].hidden = True
        blackjack_dealer = self.dealer.has_blackjacked()

        # each player gets 2 cards
        for key in self.players.keys():
            self.players[key].get_cards(self.deck.draw_card())
            self.players[key].get_cards(self.deck.draw_card())
            blackjack_player = self.players[key].has_blackjacked()
            
            # if dealer blackjacks
            if blackjack_dealer:
                # if player didn't blackjack, they lose
                if not blackjack_player:
                    self.players[key].has_won = 0
                    self.players[key].bet = 0
                # if player blackjack, they tie
                else:
                    self.players[key].has_won = 1
                    self.players[key].money += self.players[key].bet
                    self.players[key].bet = 0
            # if player blackjacks and dealer doesn'ts
            elif blackjack_player:
                print(f'{self.players[key].name} has Blackjacked')
                self.players[key].has_won = 2
        
        if blackjack_dealer:
            print(f'Dealer Blackjacked')
            self.scene = 3
            self.dealer.cards[1].hidden = False

    def hit(self, player_id):
        keys = list(self.players.keys())
        curr_turn = keys[self.current_turn_idx]
        if str(player_id) != curr_turn or self.players[curr_turn].has_busted:
            return
        self.add_card(player_id)

        self.players[curr_turn].check_busted()
        

    def stand(self, player_id):
        keys = list(self.players.keys())
        curr_turn = keys[self.current_turn_idx]
        if str(player_id) != curr_turn:
            return
        self.next_turn()

    def dealers_turn(self):
        dealer = self.dealer
        dealer.cards[1].hidden = False

        total_dealer = dealer.get_card_total()
        while total_dealer < 17:
            dealer.get_cards(self.deck.draw_card())
            total_dealer = dealer.get_card_total()

        # calculate winners
        for key in self.players.keys():
            player = self.players[key]
            total_player = player.get_card_total()
            # if player bust or player total < dealer total, lose the bet
            if player.has_busted or total_player < total_dealer <= 21:
                player.has_won = 0

            # if player ties with dealer, take the bet
            elif total_player == total_dealer:
                player.money += player.bet
                player.has_won = 1

            # if player is higher than dealer, double the bet
            elif total_player > total_dealer or total_dealer > 21:
                player.money += 2*player.bet
                player.has_won = 2
            
            player.bet = 0

    def add_card(self, player_id):
        """Draws a card for a given player

        Args:
            player_id (int): player_id

        Returns:
            int: 0 if the card is successfully drawn, -1 if the player has already busted
        """
        self.does_player_exists(player_id)
        if self.players[str(player_id)].get_card_total() > 21:
            return -1
        self.players[str(player_id)].get_cards(self.deck.draw_card())
        return 0

    def reset(self, player_id):
        self.does_player_exists(player_id)
        if self.players[str(player_id)].is_ready:
            return
        self.players[str(player_id)].is_ready = True
        if self.is_all_player_ready():
            self.reset_has_won()
            self.reset_busted()
            self.current_turn_idx = None
            # clear dealers and players hand
            self.dealer.cards = []

            for key in self.players.keys():
                self.players[key].cards = []

            # reset deck
            self.deck.reset_deck()

            self.scene = 0
            self.reset_ready()

    def does_player_exists(self, player):
        """Check if player exists

        Args:
            player (int): player ID

        Raises:
            TypeError: When player ID doesn't exists
        """
        if str(player) not in self.players.keys():
            raise TypeError('No player found')


class Player:
    def __init__(self, username, money=DEFAULT_MONEY):
        """Player class

        Args:
            username (str): username of the player joined
            money (int, optional): amount of cash that the player has. Defaults to DEFAULT_MONEY.
        """
        self.name = username
        self.money = money
        self.bet = 0
        self.is_ready = False
        self.cards = []
        self.has_busted = False 
        self.has_won = None     # 0 --> lost, 1 --> tie, 2 --> won

    def check_busted(self):
        total = self.get_card_total()
        if total > 21:
            self.has_busted = True
    
    def get_card_total(self):
        if len(self.cards) == 0:
            return
        total = 0
        aces = 0
        for card in self.cards:
            if card.value == 1:
                aces += 1
            total += min(card.value, 10)
        while aces != 0:
            if total+10 > 21:
                break
            total += 10
            aces -= 1
        return total 
    
    def get_cards(self, card):
        """Add Card for the player

        Args:
            card (Card): card to be added to the hand
        """
        self.cards.append(card)

    def has_blackjacked(self):
        assert len(self.cards) == 2
        return self.get_card_total() == 21
    

class Dealer:
    def __init__(self):
        self.cards = []

    def get_cards(self, card):
        self.cards.append(card)
    
    def get_card_total(self):
        if len(self.cards) == 0:
            return
        total = 0
        aces = 0
        for card in self.cards:
            if card.value == 1:
                aces += 1
            total += min(card.value, 10)
        while aces != 0:
            if total+10 > 21:
                break
            total += 10
            aces -= 1
        return total

    def has_blackjacked(self):
        assert len(self.cards) == 2
        return self.get_card_total() == 21


class Deck:
    def __init__(self):
        self.cards_lst = self.gen_cards()
        self.cards_lst[-3].value = 1
        self.cards_lst[-4].value = 10

    def reset_deck(self):
        self.cards_lst = self.gen_cards()

    def gen_cards(self):
        suits = ['diamond', 'club', 'heart', 'spade']
        return [Card(val, suit) for suit in suits for val in range(1, 14)]
    
    def shuffle_deck(self):
        random.shuffle(self.cards_lst)

    def draw_card(self):
        assert len(self.cards_lst) != 0, 'Deck is empty'
        return self.cards_lst.pop()


class Card:
    def __init__(self, value, suit):
        """Card Class that's stored in Deck

        Args:
            value (int): value of the card
            suit (str): suit of the card
        """
        self.value = value
        self.suit = suit
        self.hidden = False

    def __str__(self):
        if self.hidden:
            return 'red_joker'
        if self.value == 1:
            val = 'ace'
        elif self.value == 11:
            val = 'jack'
        elif self.value == 12:
            val = 'queen'
        elif self.value == 13:
            val = 'king'
        else:
            val = self.value
        return f'{val}_of_{self.suit}s'


def test():
    game = BlackjackTable()
    p1 = Player('Emma')
    p2 = Player('Jackie')

    game.join(p1)
    game.join(p2)

    game.deal_cards_init()

    print('Dealer\'s Cards: ')
    print(game.dealer.cards[0])
    print(game.dealer.cards[1])
    print(f'Dealer\'s Value: {game.dealer.get_card_total()}')
    print()

    print('Player1\'s Cards: ')
    print(game.players['0'].cards[0])
    print(game.players['0'].cards[1])
    print(f"Player1\'s Value: {game.players['0'].get_card_total()}")
    print()

    print('Player2\'s Cards: ')
    print(game.players['1'].cards[0])
    print(game.players['1'].cards[1])
    print(f"Player2\'s Value: {game.players['1'].get_card_total()}")
    print()

    game.add_card(0)
    print('Player1\'s Added Cards: ')
    print(game.players['0'].cards[0])
    print(game.players['0'].cards[1])
    print(game.players['0'].cards[2])
    print(f"Player1\'s Value: {game.players['0'].get_card_total()}")
    print()


if __name__ == "__main__":
    test()