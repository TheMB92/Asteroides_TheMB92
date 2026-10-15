import pygame
import circleshape
import shot
from constants import *

unit_vector = pygame.Vector2(0,1)

class Player(circleshape.CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cd_counter: float = 0
        self.shot_rate: int = PLAYER_SHOT_CD_RATE
        self.shot_speed: int = PLAYER_SHOT_SPEED
        self.shot_pen_count = 1
        self.powered_up_count = 0


    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, pygame.Color(50,200,200), self.triangle(), LINE_WIDTH)

    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_RATE * dt

    def move(self,dt) -> None:
        rotated_vector = unit_vector.rotate(self.rotation)
        self.velocity = rotated_vector * PLAYER_MOVE_RATE
        self.position += self.velocity * dt
        if dt > 0:
            self.direction = 1
        else:
            self.direction = -1

    def shoot(self) -> None:
        rotated_vector = unit_vector.rotate(self.rotation)
        bullet = shot.Shot(self.position[0],self.position[1],self.shot_pen_count)
        bullet.velocity = (rotated_vector * self.shot_speed) + (self.velocity * self.direction)

    def inbounds(self) -> None:
        if self.position.x >= SCREEN_WIDTH:
            self.position.x = SCREEN_WIDTH
        if self.position.x <= 0:
            self.position.x = 0
        if self.position.y >= SCREEN_HEIGHT:
            self.position.y = SCREEN_HEIGHT
        if self.position.y <= 0:
            self.position.y = 0

    def update(self, dt: float) -> None:
        self.inbounds()
        self.shot_cd_counter -= dt
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if not keys[pygame.K_w] and not keys[pygame.K_s]:
            self.velocity = pygame.Vector2(0,0)
        if keys[pygame.K_SPACE]:
            if self.shot_cd_counter > 0:
                return
            self.shot_cd_counter = 60 / self.shot_rate
            self.shoot()