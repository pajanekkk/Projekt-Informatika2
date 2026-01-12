"""
Slouzi pro funkce strileni bosse
"""
import pygame
from src.settings import *


class BossBullet:
    """
    Trida pro strelu od bosse
    """
    def __init__(self, x: int, y: int, dx: int = 0) -> None:

        self.rect = pygame.Rect(x - 6, y, 12, 18)
        self.speed_y = 300
        self.speed_x = dx


    def update(self, dt: float):
        """
        update funkce
        """
        self.rect.y += int(self.speed_y * dt)
        self.rect.x += int(self.speed_x * dt)

    def is_offscreen(self) -> bool:
        """
        kontrola if mimo obrazovku
        """
        return self.rect.top > WINDOW_HEIGHT
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        vykresleni strely bosse
        """
        pygame.draw.rect(surface, BOSS_BULL_COL, self.rect)