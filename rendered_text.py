import pygame
from constants import POINTS_PER_SEC
from pygame import freetype


pygame.freetype.init()
score_font = freetype.SysFont(freetype.get_default_font(),14)

class Rendered_Text(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]
    
    def __init__(self, text, x: float, y: float) -> None:
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()
        self.text = text
        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.pos = (x,y)

    def update(self, dt: float) -> None:
        return
    def draw(self, screen: pygame.Surface) -> None:
        pass


class Rendered_Score(Rendered_Text):
    def __init__(self, score: float, x: float, y: float) -> None:
        super().__init__(score,x,y)
        self.score = float(score)
        

    def update(self, dt: float) -> None:
        self.score += dt * POINTS_PER_SEC

    def draw(self, screen: pygame.Surface) -> None:
        roundedscore = int(self.score)
        freetype.Font.render_to(score_font,screen,self.pos,"Score:"+str(roundedscore),"white",None,0,0,30)