import random

# const
MAX_PLAYERS = 5
DEFAULT_MONEY = 100

class BlackjackTable:
    def __init__(self):
        self.players = {}           # players in the game
        self.deck = Deck()          # deck of cards
        self.deck.shuffle_deck()
        self.current_turn = None    # who's turn is it
        self.dealer = Dealer()      # dealer's set of cards
        self.scene = 0              # current scene
        self.total_ready = 0        # total number of players ready

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
        self.players[str(id)] = player
        return 0, id

    def disconnect(self, player):
        """Disconnects the player from the game

        Args:
            player (int): player ID
        """
        self.does_player_exists(player)
        if self.players[str(player)].is_ready:
            self.total_ready -= 1
        del self.players[str(player)]

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
        """Reset the ready counts
        """
        for key in self.players.keys():
            self.players[key].is_ready = False
        self.total_ready = 0

    def player_ready(self, player):
        """Sets the player status to ready when in lobby

        Args:
            player (int): player ID
        """
        self.does_player_exists(player)
        if self.players[str(player)].is_ready:
            return
        self.players[str(player)].is_ready = True
        self.total_ready += 1

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
        self.total_ready += 1

        if self.is_all_player_ready():
            self.scene = 2
    
    def deal_cards_init(self):
        """Give dealer and all players 2 cards
        """
        self.deck.shuffle_deck()

        # Dealer gets 2 cards
        self.dealer.get_cards(self.deck.draw_card())
        self.dealer.get_cards(self.deck.draw_card())

        # each player gets 2 cards
        for key in self.players.keys():
            self.players[key].get_cards(self.deck.draw_card())
            self.players[key].get_cards(self.deck.draw_card())
    
    def add_card(self, player_id):
        """Draws a card for a given player

        Args:
            player_id (int): player_id

        Returns:
            int: 0 if the card is successfully drawn, -1 if the player has already busted
        """
        assert str(player_id) in self.players.keys()
        if self.players[str(player_id)].get_card_total() > 21:
            return -1
        self.players[str(player_id)].get_cards(self.deck.draw_card())
        return 0

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
    
    def get_card_total(self):
        """Finds the total

        Returns:
            tuple: total1 and total2 
        """
        if len(self.cards) == 0:
            return
        total1 = 0
        total2 = 0
        for card in self.cards:
            if card.value == 1:
                total1 += 1
                total2 += 11
            else:
                total1 += min(card.value, 10)
                total2 += min(card.value, 10)
        if (total2 > 21):
            return total1
        return total2
    
    def get_cards(self, card):
        """Add Card for the player

        Args:
            card (Card): card to be added to the hand
        """
        self.cards.append(card)
    

class Dealer:
    def __init__(self):
        self.cards = []

    def get_cards(self, card):
        self.cards.append(card)
    
    def get_card_total(self):
        """Finds the total

        Returns:
            int: total of the cards 
        """
        if len(self.cards) == 0:
            return
        total1 = 0
        total2 = 0
        for card in self.cards:
            if card.value == 1:
                total1 += 1
                total2 += 11
            else:
                total1 += min(card.value, 10)
                total2 += min(card.value, 10)
        if (total2 > 21):
            return total1
        return total2


class Deck:
    def __init__(self):
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

    def __str__(self):
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
