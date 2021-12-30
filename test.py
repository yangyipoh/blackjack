import pygame
from blackjack import *

WIDTH = 745
HEIGHT = 600

# colours
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

class Button:
    def __init__(self, text, x, y, width=120, height=50, colour=(255, 0, 0), text_colour=(255, 255, 255), font_size=30):
        """function to create a button on the screen

        Args:
            text (str): text in the button
            x (int): x coord of the top left button
            y (int): y coord of the top left button
            width (int, optional): width of the button. Defaults to 150.
            height (int, optional): height of the button. Defaults to 100.
            colour (tuple, optional): colour of the button. Defaults to (255, 0, 0).
            text_colour (tuple, optional): colour of hte text inside. Defaults to (255, 255, 255).
            font_size (int, optional): size of the text. Defaults to 40.
        """
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.text_colour = text_colour
        self.font_size = font_size

    def draw(self, surface):
        """Draw the button of the screen

        Args:
            surface (pygame.surface): surface to be drawn
        """
        pygame.draw.rect(surface, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont('comicsans', self.font_size)
        text = font.render(self.text, 1, self.text_colour)
        x_center = self.x + round(self.width/2) - round(text.get_width()/2)
        y_center = self.y + round(self.height/2) - round(text.get_height()/2)
        surface.blit(text, (x_center, y_center))

    def click(self, pos):
        """Checks if the button is clicked

        Args:
            pos (tuple): Position of the mouse

        Returns:
            Bool: True if the button is clicked
        """
        if self.x <= pos[0] <= self.x+self.width and self.y <= pos[1] <= self.y+self.height:
            return True
        return False
    
    def get_val(self):
        return self.text


def draw(surface, buttons, scene, player, game):
    surface.fill((0, 0, 0))

    # var
    font = pygame.font.SysFont('comicsans', 25)
    box_width = 125
    box_height = 150
    offset = 20

    # rectangle for the dealer
    pygame.draw.rect(surface, RED, ((box_width*2+offset*3), 40, box_width, box_height), width=1)

    # dealer cards
    cards = game.dealer.cards
    for j, card in enumerate(cards):
        card_img = pygame.image.load(f'asset/cards/{card}.png')
        card_img = pygame.transform.scale(card_img, (83, 121))
        x = (box_width*2+offset*3) + 20
        y = 40+15*j
        surface.blit(card_img, (x, y))
    
    # rectangle for the players
    for i in range(5):
        pygame.draw.rect(surface, RED, (offset+(offset+box_width)*i, 300, box_width, box_height), width=1)

    for i in range(5):
        # connected players
        if str(i) in game.players.keys():
            player_data = game.players[str(i)]
            
            # player name
            text = font.render(player_data.name, 1, WHITE)
            x_center = offset+(offset+box_width)*i + round(box_width/2) - round(text.get_width()/2)
            y_center = 230
            surface.blit(text, (x_center, y_center))

            # player cash
            money_str = f'${player_data.money}'
            text = font.render(money_str, 1, WHITE)
            x_center = offset+(offset+box_width)*i + round(box_width/2) - round(text.get_width()/2)
            y_center = 260
            surface.blit(text, (x_center, y_center))

            # player card
            cards = player_data.cards
            for j, card in enumerate(cards):
                card_img = pygame.image.load(f'asset/cards/{card}.png')
                card_img = pygame.transform.scale(card_img, (83, 121))
                x = offset+(offset+box_width)*i+20
                y = 300+15*j
                surface.blit(card_img, (x, y))

            # if scene 1, show bets
            if scene == 1 and player == i:
                gap_width = 210
                gap_height = 50
                bet_str = f'${player_data.bet}'
                text = font.render(bet_str, 1, WHITE)
                x_center = 140 + round(gap_width/2) - round(text.get_width()/2)
                y_center = 530 + round(gap_height/2) - round(text.get_height()/2)
                surface.blit(text, (x_center, y_center))


        # waiting for players
        else:
            text = font.render('Waiting...', 1, WHITE)
            x_center = offset+(offset+box_width)*i + round(box_width/2) - round(text.get_width()/2)
            y_center = 230
            surface.blit(text, (x_center, y_center))

    # buttons
    for btn in buttons:
        btn.draw(surface)
    pygame.display.update()


def main():
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Blackjack')
    icon = pygame.image.load('asset/blackjack.png')
    pygame.display.set_icon(icon)
    pygame.font.init()
    clock = pygame.time.Clock()
    btns0 = [Button('Ready', 600, 530)]
    btns1 = [Button('-', 20, 530), Button('+', 350, 530), Button('Bet', 600, 530)]
    btns2 = [Button('Hit', 165, 530), Button('Stand', 455, 530)]
    btns3 = [Button('Continue', 600, 530)]
    scene = 3

    game = BlackjackTable()
    p1 = Player('Mandy')
    p2 = Player('Janice')
    game.join(p1)
    game.join(p2)
    p1.cards = [Card(5, 'club'), Card(7, 'heart'), Card(7, 'heart'), Card(7, 'heart'), Card(7, 'heart'), Card(7, 'heart')]
    p2.cards = [Card(11, 'heart'), Card(1, 'spade')]
    game.dealer.cards = [Card(5, 'club'), Card(7, 'heart')]

    player = 0
    
    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos):
                        print(btn.get_val())
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    scene = (scene+1)%4
                    print(scene)

        if scene == 0:
            btns = btns0
        elif scene == 1:
            btns = btns1
        elif scene == 2:
            btns = btns2
        elif scene == 3:
            btns = btns3
        draw(surface, btns, scene, player, game)


if __name__ == '__main__':
    main()