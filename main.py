import pygame
import player
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock  = pygame.time.Clock()
    dt     = 0.0
    first_player = player.Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    while True:
        log_state()
        pygame.Surface.fill(screen, pygame.Color(0,0,0))
        first_player.update(dt)
        first_player.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                     return
                pass







if __name__ == "__main__":
    main()
