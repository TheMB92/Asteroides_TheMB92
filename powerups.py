import pygame
from constants import *
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
        self.position = pygame.Vector2(x,y)
        self.color = pygame.Color(0,0,0)
        self.velocity = pygame.Vector2(0,0)
        self.rect = pygame.Rect(
            x,y,
            UPGRADE_SIZE,UPGRADE_SIZE)
        self.collision_box = (x,x+UPGRADE_SIZE,y,y+UPGRADE_SIZE)
        
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen,self.color,self.rect,0)

    def inbounds(self) -> None:
        if self.position.x >= SCREEN_WIDTH + (UPGRADE_SIZE * 5):
            self.kill()
        if self.position.x <= 0 - (UPGRADE_SIZE * 5):
            self.kill()
        if self.position.y >= SCREEN_HEIGHT + (UPGRADE_SIZE * 5):
            self.kill()
        if self.position.y <= 0 - (UPGRADE_SIZE * 5):
            self.kill()

    def update(self, dt: float) -> None:
        self.inbounds()
        self.position += (self.velocity * dt)
        self.rect.topleft = self.position

    def collides_with(self, player: player.Player) -> bool:
        min_x = max(self.rect.x,min(player.position[0], (self.rect.x + UPGRADE_SIZE)))
        min_y = max(self.rect.y,min(player.position[1], (self.rect.y + UPGRADE_SIZE)))
        if player.position.distance_to((min_x,min_y)) < player.radius:
            return True
        return False

    def upgrade(self,player: player.Player):
        pass

    def maxed(self,player) -> bool:
        return False

class RateUpgrade(PowerUP):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)
        self.color = SHOT_RATE_COLOR

    def maxed(self, player: player.Player) -> bool:
        if player.shot_rate >= MAX_SHOT_RATE:
            return True
        return False

    def upgrade(self, player: player.Player):
        logger.log_event("shot_rate_upgrade")
        self.kill
        player.shot_rate = min(MAX_SHOT_RATE, player.shot_rate + UPGRADE_SHOT_RATE)

class SpeedUpgrade(PowerUP):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)
        self.color = SHOT_SPEED_COLOR

    def maxed(self, player: player.Player) -> bool:
        if player.shot_speed >= MAX_SHOT_SPEED:
            return True
        return False

    def upgrade(self, player: player.Player):
        logger.log_event("shot_speed_upgrade")
        self.kill
        player.shot_speed = min(MAX_SHOT_SPEED, player.shot_speed + UPGRADE_SHOT_SPEED)

class PenUpgrade(PowerUP):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)
        self.color = SHOT_PEN_COLOR

    def maxed(self, player: player.Player) -> bool:
        if player.shot_pen_count >= MAX_SHOT_PEN_COUNT:
            return True
        return False

    def upgrade(self, player: player.Player):
        logger.log_event("shot_pen_upgrade")
        self.kill
        player.shot_pen_count = min(MAX_SHOT_PEN_COUNT, player.shot_pen_count + UPGRADE_SHOT_PEN_COUNT)
