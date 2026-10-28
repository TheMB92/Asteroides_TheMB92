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
        self.pen = f"Pen:{player.shot_pen_count}"
        self.shot_speed = f"MV:{int(player.shot_speed / SCALE)} m/s"
        self.fire_rate = f"Rate:{player.shot_rate} RPM"

    def refresh(self,player: Player) -> None:
        self.player = player

    def update(self, dt: float) -> None:
        if self.player.shot_pen_count < MAX_SHOT_PEN_COUNT:
            self.pen = f"Pen:{self.player.shot_pen_count}"
        else:
            self.pen = f"Pen:{MAX_SHOT_PEN_COUNT}(Max)"
        if self.player.shot_speed < MAX_SHOT_SPEED:
            self.shot_speed = f"MV:{int(self.player.shot_speed / SCALE)} m/s"
        else:
            self.shot_speed = f"MV:{int(self.player.shot_speed / SCALE)} m/s(Max)"
        if self.player.shot_rate < MAX_SHOT_RATE:
            self.fire_rate = f"Rate:{int(self.player.shot_rate)} RPM"
        else:
            self.fire_rate = f"Rate:{int(self.player.shot_rate)} RPM(Max)"

    def draw(self, screen: pygame.Surface) -> None:
        freetype.Font.render_to(
            general_font,screen,(self.position.x,self.position.y),
            f"{self.shot_speed}",
            SHOT_SPEED_COLOR,None,0,0,0)
        freetype.Font.render_to(
            general_font,screen,(self.position.x+270,self.position.y),
            f"{self.fire_rate}",
            SHOT_RATE_COLOR,None,0,0,0)
        freetype.Font.render_to(
            general_font,screen,(self.position.x+600,self.position.y),
            f"{self.pen}",
            SHOT_PEN_COLOR,None,0,0,0)

class Main_Menu_Text(Rendered_Text):
    def __init__(self, x: float, y: float, score: int, firstgame : bool, last_player: player.Player) -> None:
        self.score = score
        self.firstgame = firstgame
        self.last_player = last_player
        super().__init__(x, y)
    def draw(self, screen: pygame.Surface) -> None:
        freetype.Font.render_to(
            general_font,screen,(self.position.x - (263 * SCALE),self.position.y- (SCREEN_HEIGHT/3)),
            "Asteroids by TheMB92",
            "white",None,0,0,50*SCALE)
        freetype.Font.render_to(
                    general_font,screen,(self.position.x - (250 * SCALE),self.position.y - ((SCREEN_HEIGHT/3)-200*SCALE)),
                    'Press "N" to start a new game',
                    "white",None,0,0,0*SCALE)
        freetype.Font.render_to(
                    general_font,screen,(self.position.x - (250 * SCALE),self.position.y - ((SCREEN_HEIGHT/3)-230*SCALE)),
                    'Press "Q" to quit game',
                    "white",None,0,0,0*SCALE)

        if not self.firstgame:
            freetype.Font.render_to(
                general_font,screen,(self.position.x - (150 * SCALE),self.position.y- ((SCREEN_HEIGHT/3)-100*SCALE)),
                "GAME OVER",
                "red",None,0,0,50*SCALE)
            freetype.Font.render_to(
                                general_font,screen,(self.position.x - (250 * SCALE),self.position.y - ((SCREEN_HEIGHT/3)-290*SCALE)),
                                "Last Round Results:",

                                "white",None,0,0,0*SCALE)
            freetype.Font.render_to(
                                general_font,screen,(self.position.x - (220 * SCALE),self.position.y - ((SCREEN_HEIGHT/3)-320*SCALE)),
                                f'Score: {self.score}',
                                "white",None,0,0,0*SCALE)
            freetype.Font.render_to(
                                general_font,screen,(self.position.x - (220 * SCALE),self.position.y - ((SCREEN_HEIGHT/3)-350*SCALE)),
                                f"Muzzle Velocity: {int(self.last_player.shot_speed / SCALE)} m/s",
                                SHOT_SPEED_COLOR,None,0,0,0*SCALE)
            freetype.Font.render_to(
                                general_font,screen,(self.position.x - (220 * SCALE),self.position.y - ((SCREEN_HEIGHT/3)-380*SCALE)),
                                f"Rate: {int(self.last_player.shot_rate)} RPM",
                                SHOT_RATE_COLOR,None,0,0,0*SCALE)
            freetype.Font.render_to(
                                general_font,screen,(self.position.x - (220 * SCALE),self.position.y - ((SCREEN_HEIGHT/3)-410*SCALE)),
                                f"Pen: {self.last_player.shot_pen_count}",
                                SHOT_PEN_COLOR,None,0,0,0*SCALE)
            freetype.Font.render_to(
                                general_font,screen,(self.position.x - (220 * SCALE),self.position.y - ((SCREEN_HEIGHT/3)-440*SCALE)),
                                f"Total Power-Ups: {self.last_player.powered_up_count}",
                                "white",None,0,0,0*SCALE)