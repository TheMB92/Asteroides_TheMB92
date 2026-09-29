import pygame
import player
from asteroid import Asteroid
import sys
import asteroidfield
from logger import log_event
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    player.Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    asteroidfield.AsteroidField.containers = (updatable)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock  = pygame.time.Clock()
    dt     = 0.0
    the_asteroid_field = asteroidfield.AsteroidField()
    first_player = player.Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    testroid = Asteroid(-10,-10,5)
    while True:
        log_state()
        pygame.Surface.fill(screen, pygame.Color(0,0,0))
        updatable.update(dt)
        for asteroid in asteroids:
            if asteroid.collides_with(first_player):
                log_event("player_hit")
                print("Game Over!")
                sys.exit() 
        
        for sprite in drawable:
            sprite.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                     return
                pass

if __name__ == "__main__":
    main()
