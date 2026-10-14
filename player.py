import pygame
import circleshape
import shot
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_RATE, PLAYER_MOVE_RATE, PLAYER_SHOT_SPEED, PLAYER_SHOT_CD_SEC

class Player(circleshape.CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cd_counter: float = 0
        self.shot_cd: float = PLAYER_SHOT_CD_SEC
        self.shot_speed: float = PLAYER_SHOT_SPEED
        self.shot_pen_count = 1


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
        unit_vector = pygame.Vector2(0,1)
        rotated_vector = unit_vector.rotate(self.rotation)
        self.velocity = rotated_vector * PLAYER_MOVE_RATE * dt
        self.position += self.velocity

    def shoot(self) -> None:
        bullet = shot.Shot(self.position[0],self.position[1],self.shot_pen_count)
        unit_vector = pygame.Vector2(0,1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotates_with_speed_vector = rotated_vector * self.shot_speed
        bullet.velocity = rotates_with_speed_vector + (self.velocity*15)


    def update(self, dt: float) -> None:
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
        if keys[pygame.K_SPACE]:
            if self.shot_cd_counter > 0:
                return
            self.shot_cd_counter = self.shot_cd
            self.shoot()