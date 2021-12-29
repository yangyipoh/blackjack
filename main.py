import pygame

WIDTH = 800
HEIGHT = 600
 
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Blackjack')
    icon = pygame.image.load('asset/blackjack.png')
    pygame.display.set_icon(icon)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        


if __name__ == '__main__':
    main()
