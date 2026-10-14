import pygame
import player
import shot
import rendered_text
from asteroid import Asteroid
import sys
import asteroidfield
import shot_upgrades
from constants import SCREEN_WIDTH, SCREEN_HEIGHT,POINTS_PER_ASTEROID_HIT, POINTS_PER_SEC
import logger

def closegame(score):
        final_score = int(score)
        print("Game Over!")
        print(f"Score: {final_score}") 
        sys.exit()


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    updatable = pygame.sprite.Group()
    drawable  = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots     = pygame.sprite.Group()
    powerups  = pygame.sprite.Group()
    player.Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    asteroidfield.AsteroidField.containers = (updatable)
    shot.Shot.containers = (updatable, drawable, shots)
    rendered_text.Rendered_Score.containers = (updatable, drawable)
    shot_upgrades.PowerUP.containers = (updatable, drawable, powerups)
    score = rendered_text.Rendered_Score(0.0,0,0)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock  = pygame.time.Clock()
    dt     = 0.0
    the_asteroid_field = asteroidfield.AsteroidField()
    player1 = player.Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    testupgrade = shot_upgrades.PenUpgrade(SCREEN_HEIGHT/3, SCREEN_HEIGHT/3)
    while True:
        logger.log_state()
        pygame.Surface.fill(screen, pygame.Color(0,0,0))
        updatable.update(dt)
        for asteroid in asteroids:
            for bullet in shots:
                 if asteroid.collides_with(bullet):
                      logger.log_event("asteroid_shot")
                      score.score += POINTS_PER_ASTEROID_HIT
                      bullet.pen_count -= 1
                      if bullet.pen_count < 1:
                        bullet.kill()
                      asteroid.split()
            if asteroid.collides_with(player1):
                closegame(score.score)
        for powerup in powerups:
             if powerup.collides_with(player1):
                  powerup.upgrade(player1)
                  powerup.kill()
        for sprite in drawable:
            sprite.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            closegame(score.score)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    closegame(score.score)
                pass

if __name__ == "__main__":
    main()
