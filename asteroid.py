import circleshape
import pygame
import constants

class Asteroid(circleshape.CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(
            screen,
            pygame.Color(255,0,0),
            self.position,
            self.radius,
            constants.LINE_WIDTH
            )

    def update(self, dt: float) -> None:
        self.position += (self.velocity * dt)