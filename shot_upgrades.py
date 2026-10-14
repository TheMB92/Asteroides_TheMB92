import pygame
import constants
from logger import log_event
import player
import random

class Upgrade(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float,) -> None:
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()
        self.color = pygame.Color(0,0,0)
        self.velocity = (random.randint(-1,1),random.randint(-1,1))
        self.rect = pygame.Rect(x,y,constants.UPGRADE_SIZE, constants.UPGRADE_SIZE)
        self.collision_box = (x,x+constants.UPGRADE_SIZE,y,y+constants.UPGRADE_SIZE)
        
    def draw(self, screen: pygame.Surface) -> None:
        pass
    
    def update(self, dt: float) -> None:
        self.rect.move(self.velocity[0]*dt,self.velocity[1]*dt)

#    def collides_with(self, player: player.Player) -> bool:
#        collide_distance = 

class RateUpgrade(Upgrade):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)
        self.color = pygame.Color(255,255,0)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen,self.color,self.rect,constants.LINE_WIDTH)