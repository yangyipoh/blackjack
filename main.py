import pygame

WIDTH = 800
HEIGHT = 600

class Button:
    def __init__(self, text, x, y, width=150, height=100, colour=(255, 0, 0), text_colour=(255, 255, 255), font_size=40):
        """function to create a button on the screen

        Args:
            text (str): text in the button
            x (int): x coord of the top left button
            y (int): y coord of the top left button
            width (int, optional): [description]. Defaults to 150.
            height (int, optional): [description]. Defaults to 100.
            colour (tuple, optional): [description]. Defaults to (255, 0, 0).
            text_colour (tuple, optional): [description]. Defaults to (255, 255, 255).
            font_size (int, optional): [description]. Defaults to 40.
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
        pygame.draw.rect(surface, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont('comicsans', self.font_size)
        text = font.render(self.text, 1, self.text_colour)
        x_center = self.x + round(self.width/2) - round(text.get_width()/2)
        y_center = self.y + round(self.height/2) - round(text.get_height()/2)
        surface.blit(text, (x_center, y_center))

    def click(self, pos):
        if self.x <= pos[0] <= self.x+self.width and self.y <= pos[1] <= self.y+self.height:
            return True
        return False


def draw(surface, btn):
    surface.fill((0, 0, 0))
    btn.draw(surface)
    pygame.display.update()

 
def main():
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Blackjack')
    icon = pygame.image.load('asset/blackjack.png')
    pygame.display.set_icon(icon)
    pygame.font.init()

    btn = Button('Test', 0, 0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if btn.click(pos):
                    print('Clicked')
        
        draw(surface, btn)
        


if __name__ == '__main__':
    main()
