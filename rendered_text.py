import pygame
from constants import *
from pygame import freetype
from player import Player
from powerups import *


pygame.freetype.init()
general_font = freetype.SysFont(freetype.get_default_font(),30)

class Rendered_Text(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]
    
    def __init__(self, x: float, y: float) -> None:
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()
        self.position: pygame.Vector2 = pygame.Vector2(x, y)

    def update(self, dt: float) -> None:
        return
    def draw(self, screen: pygame.Surface) -> None:
        pass


class Rendered_Score(Rendered_Text):
    def __init__(self, score: float, x: float, y: float) -> None:
        super().__init__(x,y)
        self.score = float(score)
        

    def update(self, dt: float) -> None:
        self.score += dt * POINTS_PER_SEC

    def draw(self, screen: pygame.Surface) -> None:
        roundedscore = int(self.score)
        freetype.Font.render_to(general_font,screen,
        (self.position.x,self.position.y),
        "Score:"+str(roundedscore),
        "white",None,0,0,0)

class Rendered_Stats(Rendered_Text):
    def __init__(self,player: Player, x: float, y: float) -> None:
        super().__init__(x,y)
        self.pen = f"F.Pen:{player.shot_pen_count}"
        self.shot_speed = f"F,Spd:{player.shot_speed}"
        self.fire_rate = f"F.Rate:{1000 / player.shot_cd}"

    def refresh(self,player: Player) -> None:
        self.player = player

    def update(self, dt: float) -> None:
        if self.player.shot_pen_count < MAX_SHOT_PEN_COUNT:
            self.pen = f"F.Pen:{self.player.shot_pen_count}"
        else:
            self.pen = f"F.Pen:{MAX_SHOT_PEN_COUNT}(Max)"
        if self.player.shot_speed < MAX_SHOT_SPEED:
            self.shot_speed = f"F.Spd:{self.player.shot_speed}"
        else:
            self.shot_speed = f"F.Spd:{self.player.shot_speed}(Max)"
        if self.player.shot_cd > MIN_SHOT_CD:
            self.fire_rate = f"F.Rate:{int(50 / self.player.shot_cd)}"
        else:
            self.fire_rate = f"F.Rate:{int(50 / self.player.shot_cd)}(Max)"

    def draw(self, screen: pygame.Surface) -> None:
        freetype.Font.render_to(
            general_font,screen,(self.position.x,self.position.y),
            f"{self.shot_speed}",
            SHOT_SPEED_COLOR,None,0,0,0)
        freetype.Font.render_to(
            general_font,screen,(self.position.x+250,self.position.y),
            f"{self.fire_rate}",
            SHOT_RATE_COLOR,None,0,0,0)
        freetype.Font.render_to(
            general_font,screen,(self.position.x+500,self.position.y),
            f"{self.pen}",
            SHOT_PEN_COLOR,None,0,0,0)