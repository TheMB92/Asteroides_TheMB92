import random
from collections.abc import Callable
import pygame
from player import Player
from powerups import *
from asteroid import Asteroid
from constants import *

Edge = tuple[pygame.Vector2, Callable[[float], pygame.Vector2]]

class SpawnField(pygame.sprite.Sprite):
    containers: pygame.sprite.Group

    edges: list[Edge] = [
        (
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ),
        (
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ),
        (
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ),
        (
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ),
    ]

    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.spawn_rate_sec = 0.0


    def spawn(
        self, size: float, position: pygame.Vector2, velocity: pygame.Vector2
    ) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def refresh(self) -> None:
        pass


class AsteroidField(SpawnField):

    def __init__(self) -> None:
        super().__init__()
        self.spawn_rate_sec = ASTEROID_SPAWN_RATE_SECONDS
        self.asteroid_kinds = ASTEROID_KINDS
        self.intensity = 0
        self.max_spd_multiplier = 3

    def spawn(
        self, radius: float, position: pygame.Vector2, velocity: pygame.Vector2
    ) -> None:
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt: float) -> None:
        self.spawn_timer += dt
        if self.spawn_timer > self.spawn_rate_sec:
            self.spawn_timer = 0
            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(ASTEROID_MIN_SPD, (ASTEROID_MIN_SPD * self.max_spd_multiplier))
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, self.asteroid_kinds)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)

    def intensify(self) -> None:
        self.spawn_rate_sec -= 0.0035
        self.intensity += 1
        
        if self.intensity >= 6:
            self.intensity = 0
            self.asteroid_kinds += 1
            self.max_spd_multiplier += 1


class PowerUpField(SpawnField):

    def __init__(self,player: Player) -> None:
        super().__init__()
        self.spawn_rate_sec = UPGRADE_SPAWN_RATE_SECONDS
        self.pen = player.shot_pen_count
        self.speed = player.shot_speed
        self.rate = player.shot_rate

    def refresh(self,player: Player) -> None:
        self.spawn_rate_sec = UPGRADE_SPAWN_RATE_SECONDS
        self.pen = player.shot_pen_count
        self.speed = player.shot_speed
        self.rate = player.shot_rate
        
    def spawn(
            self, kind, 
            position: pygame.Vector2, velocity: pygame.Vector2,
            ) -> None:
        if kind == 0:
            return None
        powerup = kind(position.x,position.y)
        powerup.velocity = velocity

    def update(self, dt: float) -> None:
        self.spawn_timer += dt
        if self.spawn_timer > self.spawn_rate_sec:
            self.spawn_timer = 0
            # spawn a new powerup at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(80, 300)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-60,60))
            position = edge[1](random.uniform(0, 1))
            kind = 0
            selector = random.randint(0,100)
            if selector <= 10 and self.pen < MAX_SHOT_PEN_COUNT:
                kind = PenUpgrade
            if selector < 50 and selector > 10 and self.rate < MAX_SHOT_RATE :
                kind = RateUpgrade
            if selector >= 50 and self.speed < MAX_SHOT_SPEED:
                kind = SpeedUpgrade
            self.spawn(kind, position, velocity)