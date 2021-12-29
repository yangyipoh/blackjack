import random

MAX_PLAYERS = 5
DEFAULT_MONEY = 100

class BlackjackTable:
    def __init__(self):
        self.players = {}
        self.deck = Deck()
        self.deck.shuffle_deck()
        self.current_turn = 0
        self.dealer = Dealer()

    def find_seat(self):
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
        id = self.find_seat()
        if id == -1:
            return -1, -1
        self.players[str(id)] = player
        return 0, id
    
    def deal_cards_init(self):
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
    
    def set_bet(self, player_id):
        pass


class Player:
    def __init__(self, username, money=DEFAULT_MONEY):
        """Player class

        Args:
            username (str): username of the player joined
            money (int, optional): amount of cash that the player has. Defaults to DEFAULT_MONEY.
        """
        self.name = username
        self.money = money
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
        self.cards.append(card)
    

class Dealer:
    def __init__(self):
        self.cards = []

    def get_cards(self, card):
        self.cards.append(card)
    
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
        return f'{self.value} of {self.suit}'


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