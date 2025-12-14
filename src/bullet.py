"""
Zpracovani střel
"""
import pygame
from src.player import *
from src.settings import *
from src.game import *

BULLET_COLOR = (255, 255, 255)

class Bullet:
    def __init__(self, start_x: float, start_y: float) -> None:
        self.rect = pygame.Rect(0, 0, BULLET_WIDTH, BULLET_HEIGHT)
        self.rect.centerx = int(start_x)
        self.rect.bottom = int(start_y)

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
        pygame.draw.rect(surface, BULLET_COLOR, self.rect)