import pygame
import player
import shot
import rendered_text
from asteroid import Asteroid
import sys
import asteroidfield
from constants import SCREEN_WIDTH, SCREEN_HEIGHT,POINTS_PER_ASTEROID_HIT, POINTS_PER_SEC
import logger

def main():
    print ()
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    updatable = pygame.sprite.Group()
    drawable  = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots     = pygame.sprite.Group()
    player.Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    asteroidfield.AsteroidField.containers = (updatable)
    shot.Shot.containers = (updatable, drawable, shots)
    rendered_text.Rendered_Score.containers = (updatable, drawable)
    score = rendered_text.Rendered_Score(0.0,0,0)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock  = pygame.time.Clock()
    dt     = 0.0
    the_asteroid_field = asteroidfield.AsteroidField()
    first_player = player.Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    while True:
        logger.log_state()
        pygame.Surface.fill(screen, pygame.Color(0,0,0))
        updatable.update(dt)
        for asteroid in asteroids:
            for bullet in shots:
                 if asteroid.collides_with(bullet):
                      logger.log_event("asteroid_shot")
                      score.score += POINTS_PER_ASTEROID_HIT
                      bullet.kill()
                      asteroid.split()
            if asteroid.collides_with(first_player):
                logger.log_event("player_hit")
                score = int(score.score)
                print("Game Over!")
                print(f"Score: {score}") 
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
