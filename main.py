import pygame
from network import Network
# from blackjack import *

WIDTH = 800
HEIGHT = 600

class Button:
    def __init__(self, text, x, y, width=150, height=100, colour=(255, 0, 0), text_colour=(255, 255, 255), font_size=30):
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
        print(pos)
        if self.x <= pos[0] <= self.x+self.width and self.y <= pos[1] <= self.y+self.height:
            return True
        return False


def draw(surface):
    surface.fill((0, 0, 0))
    pygame.display.update()

 
def main():
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Blackjack')
    icon = pygame.image.load('asset/blackjack.png')
    pygame.display.set_icon(icon)
    pygame.font.init()
    clock = pygame.time.Clock()
    n = Network('192.168.1.108')
    player = int(n.getP())
    print(f'You are: Player {player}')

    running = True
    while running:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            running = False
            print('Error when requesting board config')
            break
        
        print(game)

        # process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
        
        # display
        draw(surface)
        


if __name__ == '__main__':
    main()
