"""
Zpracovani střel
"""
import pygame
from src.player import *
from src.settings import *
from src.game import *



class Bullet:
    def __init__(self, start_x: float, start_y: float) -> None:

        self.image = pygame.image.load("assets/img/bullet2.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.rect = self.image.get_rect(x = start_x, y = start_y)
        

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
        surface.blit(self.image, self.rect)