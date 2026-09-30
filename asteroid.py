import circleshape
import pygame
import constants
from logger import log_event
import random


class Asteroid(circleshape.CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(
            screen,
            pygame.Color(0,0,255),
            self.position,
            self.radius,
            constants.LINE_WIDTH
            )

    def update(self, dt: float) -> None:
        self.position += (self.velocity * dt)

    def split(self) -> None:
        self.kill()
        if self.radius <= constants.ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        split_angle = random.uniform(20,50)
        new_vector1 = self.velocity.rotate(split_angle)
        new_vector2 = self.velocity.rotate(-split_angle)
        new_rad    = self.radius - constants.ASTEROID_MIN_RADIUS
        splitroid1 = Asteroid(self.position[0],self.position[1],new_rad)
        splitroid2 = Asteroid(self.position[0],self.position[1],new_rad)
        splitroid1.velocity = new_vector1 * 1.2
        splitroid2.velocity = new_vector2 * 1.2