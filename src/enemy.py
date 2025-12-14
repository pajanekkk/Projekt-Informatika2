"""
Slouzi k implementaci tridy pro nepritele
"""

import pygame
from src.settings import *

ENEMY_COLOR = (255, 0, 0)

class Enemy:
    def __init__(self, start_x: float, start_y: float) -> None:
        self.rect = pygame.Rect(0, 0, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.rect.centerx = int(start_x)
        self.rect.top = int(start_y)

        self.speed = ENEMY_SPEED
    
    def update(self, dt: float) -> None:
        """
        update funkce
        """
        dy = self.speed * dt
        self.rect.y += int(dy)
    
    def is_offscreen(self) -> bool:
        """
        kontrola, jestli je enemy mimo obrazovku, to same jako v bullet
        """
        return self.rect.top > WINDOW_HEIGHT
    
    def draw(self, surface: pygame.Surface) -> None:
        """
       vykresleni nepritele
        """
        pygame.draw.rect(surface, ENEMY_COLOR, self.rect)