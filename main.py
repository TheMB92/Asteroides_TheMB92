import pygame
import rendered_text
import sys
import logger
from game import *

def main():
    pygame.init()
    last_score = 0
    mainmenu = rendered_text.Main_Menu_Text(SCREEN_WIDTH/2, SCREEN_HEIGHT/2,last_score,True,None)
    while True:
        pygame.Surface.fill(screen, pygame.Color(0,0,0))
        mainmenu.draw(screen)
        pygame.display.flip()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            sys.exit()
        if keys[pygame.K_n]:
                results = game()
                last_score = results[0]
                last_player = results[1]
                mainmenu = rendered_text.Main_Menu_Text(SCREEN_WIDTH/2, SCREEN_HEIGHT/2,last_score,False,last_player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
if __name__ == "__main__":
    main()