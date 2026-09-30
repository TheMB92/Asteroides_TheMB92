import pygame
import circleshape
from constants import SHOT_RADIUS,LINE_WIDTH

class Shot(circleshape.CircleShape):
    def __init__(self,x: float,y: float) -> None:
        super().__init__(x,y,SHOT_RADIUS)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(
            screen,
            pygame.Color(255,0,0),
            self.position,
            self.radius,
            LINE_WIDTH
            )

    def update(self, dt: float) -> None:
        self.position += (self.velocity * dt)
    