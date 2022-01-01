import pygame
from network import Network
import argparse

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
    
    def get_text(self):
        """returns the text on the button

        Returns:
            str: text on button
        """
        return self.text


def preprocessing(btns_array, game, player):
    """Extract the necessary information from BlackjackTable to display the game

    Args:
        btns_array (list): List of buttons for a given scene
        game (BlackjackTable): game returned from the server
        player (int): player id

    Returns:
        tuple: (Buttons for the particular scene, which scene to display)
    """
    scene = game.scene
    btns = btns_array[scene]

    # change the colour of buttons
    if scene == 0 or scene == 3:
        if game.players[str(player)].is_ready:
            btns[0].colour = GREEN
        else:
            btns[0].colour = RED
    elif scene == 1:
        if game.players[str(player)].is_ready:
            btns[2].colour = GREEN
        else:
            btns[2].colour = RED
    elif scene == 2:
        keys = list(game.players.keys())
        curr_turn = keys[game.current_turn_idx]
        if curr_turn != str(player):
            btns[0].colour = RED
            btns[1].colour = RED
        else:
            btns[1].colour = GREEN
            if game.players[curr_turn].has_busted:
                btns[0].colour = RED
            else:
                btns[0].colour = GREEN
            
    return btns, scene


def display_error(err_code):
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f'ERROR: {err_code}')
    icon = pygame.image.load('asset/blackjack.png')
    pygame.display.set_icon(icon)
    pygame.font.init()
    clock = pygame.time.Clock()

    if err_code == -1:
        err_msg = 'Invalid Lobby ID provided'
    elif err_code == -2:
        err_msg = 'Lobby is too full'
    else:
        err_msg = 'Unknown'

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # draw on screen
        surface.fill((0, 0, 0))

        font = pygame.font.SysFont('comicsans', 25)
        text = font.render(err_msg, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        surface.blit(text, text_rect)
        pygame.display.update()


def draw(surface, buttons, scene, player, game):
    """Draw the game

    Args:
        surface (Surface): window
        buttons (list): list of buttons that needs to be rendered
        scene (int): scene that needs to be rendered
        player (int): current player
        game (BlackjackTable): game returned from the server
    """
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
        y = 40+17*j
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
                y = 300+17*j
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

            # if scene 2, show card total
            if scene == 2 and player == i:
                total = player_data.get_card_total()
                if total > 21:
                    total_str = 'Bust'
                else:
                    total_str = f'Total: {total}'
                text = font.render(total_str, 1, WHITE)
                x_center = 30
                y_center = 30
                surface.blit(text, (x_center, y_center))
                

            # if scene 3, show if player has won or lost
            if scene == 3 and player == i:
                status = player_data.has_won
                if status == 0:
                    status_str = 'Lose'
                elif status == 1:
                    status_str = 'Tie'
                elif status == 2:
                    status_str = 'Win'
                else:
                    status_str = 'Error'

                status_font = pygame.font.SysFont('comicsans', 45)
                text = status_font.render(status_str, 1, WHITE)
                x_center = 30
                y_center = 30
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
    # argparse
    parser = argparse.ArgumentParser(description='Change parameters for the game')
    parser.add_argument('-ip', '--server_ip', metavar='', type=str, required=True, help='IP address of server')
    parser.add_argument('-port', '--port_no', metavar='', type=int, default=5555, help='Port number from the server')
    parser.add_argument('-lobby', '--lobby_id', metavar='', type=str, default='', help='Lobby ID for the server')
    parser.add_argument('-name', '--usrname', metavar='', type=str, default='', help='Name used to join the server')

    args = parser.parse_args()

    SERVER_IP = args.server_ip
    PORT_NO = args.port_no
    LOBBY_ID = args.lobby_id
    USR_NAME = args.usrname

    # networking
    n = Network(SERVER_IP, port_no=PORT_NO, lobby_id=LOBBY_ID, name=USR_NAME)

    # get return message from server
    msg = int(n.getP())

    # if msg -1, -2, ....., there's an error
    if msg < 0:
        display_error(msg)
        return

    player = int(msg)
    print(f'You are: Player {player}')

    # get game state
    try:
        game = n.send("get")
    except:
        print('Error when requesting board config')

    player_name = game.players[str(player)].name

    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f'Blackjack: {player_name}')
    icon = pygame.image.load('asset/blackjack.png')
    pygame.display.set_icon(icon)
    pygame.font.init()
    clock = pygame.time.Clock()

    # buttons for the game
    btns0 = [Button('Ready', 600, 530)]
    btns1 = [Button('-', 20, 530), Button('+', 350, 530), Button('Bet', 600, 530)]
    btns2 = [Button('Hit', 165, 530), Button('Stand', 455, 530)]
    btns3 = [Button('Continue', 600, 530)]
    btn_array = [btns0, btns1, btns2, btns3]

    running = True
    while running:
        clock.tick(60)

        # get game state
        try:
            game = n.send("get")
        except:
            running = False
            print('Error when requesting board config')
            break

        # extract information
        if game == None:
            break
        
        btns, scene = preprocessing(btn_array, game, player)

        # process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # send button presses to the server
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    # send button information to server
                    if btn.click(pos):
                        n.send(btn.text)
            
            # send keyboard presses to the server
            if event.type == pygame.KEYDOWN:
                if scene == 1:
                    if event.key == pygame.K_LEFT:
                        n.send('-')
                    elif event.key == pygame.K_RIGHT:
                        n.send('+')



        # display
        draw(surface, btns, scene, player, game)
        

if __name__ == '__main__':
    main()
