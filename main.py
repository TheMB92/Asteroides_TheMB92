import pygame
import player
import shot
import rendered_text
from asteroid import Asteroid
import sys
import spawnfield
from powerups import *
from constants import *
import logger

def closegame(score,player: player.Player):
        final_score = int(score)
        print("Game Over!")
        print(f"Score: {final_score}")
        print(f"Final stats - MV:{player.shot_speed} RPM:{int(player.shot_rate)} Pen:{player.shot_pen_count} Total powerups:{player.powered_up_count} ")
        sys.exit()


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    updatable   = pygame.sprite.Group()
    drawable    = pygame.sprite.Group()
    asteroids   = pygame.sprite.Group()
    shots       = pygame.sprite.Group()
    powerups    = pygame.sprite.Group()
    player.Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    spawnfield.SpawnField.containers = (updatable)
    shot.Shot.containers = (updatable, drawable, shots)
    rendered_text.Rendered_Text.containers = (updatable, drawable)
    PowerUP.containers = (updatable, drawable, powerups)
    player1 = player.Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    score = rendered_text.Rendered_Score(0.0,0,0)
    stats = rendered_text.Rendered_Stats(player1,SCREEN_WIDTH-800,0)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock  = pygame.time.Clock()
    dt     = 0.0
    asteroid_field = spawnfield.AsteroidField()
    powerup_field  = spawnfield.PowerUpField(player1)

    while True:
        logger.log_state()
        pygame.Surface.fill(screen, pygame.Color(0,0,0))
        stats.refresh(player1)
        powerup_field.refresh(player1)
        updatable.update(dt)
        for asteroid in asteroids:
            for bullet in shots:
                if not asteroid.alive():
                    break
                if asteroid.collides_with(bullet):
                    logger.log_event("asteroid_shot")
                    score.score += POINTS_PER_ASTEROID_HIT
                    bullet.pen_count -= 1
                    if bullet.pen_count < 1:
                        bullet.kill()
                    asteroid.split()
                    break
            if asteroid.collides_with(player1) and asteroid.alive():
                closegame(score.score,player1)
        for powerup in powerups:
            if powerup.maxed(player1):
                 powerup.kill()
                 continue
            if powerup.collides_with(player1):
                powerup.upgrade(player1)
                asteroid_field.intensify()
                player1.powered_up_count += 1
        for sprite in drawable:
            sprite.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            closegame(score.score,player1)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    closegame(score.score,player1)
                pass

if __name__ == "__main__":
    main()
