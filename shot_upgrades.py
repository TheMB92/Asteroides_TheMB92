import pygame
import constants
from logger import log_event
import player
import random
import logger

class PowerUP(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float,) -> None:
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()
        self.color = pygame.Color(0,0,0)
        self.speed = random.randint(50,250)
        self.velocity = pygame.Vector2(random.uniform(-2,2),random.uniform(-2,2))
        self.rect = pygame.Rect(
            x,y,
            constants.UPGRADE_SIZE,constants.UPGRADE_SIZE)
        self.collision_box = (x,x+constants.UPGRADE_SIZE,y,y+constants.UPGRADE_SIZE)
        
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen,self.color,self.rect,0)

    def update(self, dt: float) -> None:
        self.rect.move_ip(self.velocity.x*dt*self.speed,self.velocity.y*dt*self.speed)

    def collides_with(self, player: player.Player) -> bool:
        min_x = max(self.rect.x,min(player.position[0], (self.rect.x + constants.UPGRADE_SIZE)))
        min_y = max(self.rect.y,min(player.position[1], (self.rect.y + constants.UPGRADE_SIZE)))
        if player.position.distance_to((min_x,min_y)) < player.radius:
            return True
        return False

    def upgrade(self,player: player.Player):
        pass

class RateUpgrade(PowerUP):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)
        self.color = pygame.Color(255,255,0)

    def upgrade(self, player: player.Player):
        logger.log_event("shot_rate_upgrade")
        self.kill
        player.shot_cd -= constants.UPGRADE_SHOT_RATE

class SpeedUpgrade(PowerUP):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)
        self.color = pygame.Color(255,0,255)

    def upgrade(self, player: player.Player):
        logger.log_event("shot_rate_upgrade")
        self.kill
        player.shot_speed += constants.UPGRADE_SHOT_SPEED

class PenUpgrade(PowerUP):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)
        self.color = pygame.Color(120,30,30)

    def upgrade(self, player: player.Player):
        logger.log_event("shot_rate_upgrade")
        self.kill
        player.shot_pen_count += constants.UPGRADE_SHOT_PEN_COUNT