import pygame
from pygame import color
from pygame.display import set_mode
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    while True:
        log_state()
        pygame.Surface.fill(screen, color.Color(0,0,0))
        pygame.display.flip()
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                     return
                pass







if __name__ == "__main__":
    main()
