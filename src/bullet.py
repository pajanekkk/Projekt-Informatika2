"""
Zpracovani střel
"""
import pygame
from src.player import *
from src.settings import *
from src.game import *



class Bullet:
    """
    Trida pro strelu
    """
    # nacitam na urovni tridy, at nemusim pri kazdem vystrelu nacitat obrazek
    image = pygame.image.load("assets/img/bullet.png")
    image = pygame.transform.scale(image, (30, 50))

    def __init__(self, start_x: float, start_y: float) -> None:
        """
        start_x, start_y - pocatecni pozice
        """
        self.rect = Bullet.image.get_rect(centerx = start_x, y = start_y)
        self.speed = BULLET_SPEED
    
    def update(self, dt: float) -> None:
        """
        proste update funkce lol
        """
        dy = -self.speed * dt # dy je vertikalni osa
        self.rect.y += int(dy)

    def is_offscreen(self) -> bool:
        """
        pokud je strela mimo obrazovku, vrati True
        """
        return self.rect.bottom < 0
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        vykresleni strely
        """
        surface.blit(Bullet.image, self.rect)