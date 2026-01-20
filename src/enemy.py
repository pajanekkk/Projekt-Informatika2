"""
Slouzi k implementaci tridy pro nepritele
"""

import pygame
import random
from src.settings import *



class Enemy:
    """
    Trida pro nepritele
    """
    def __init__(self, start_x: float, start_y: float, speed_mult=1.0) -> None:
        """
        start_x, start_y - pocatecni pozice
        """
        self.image = pygame.image.load("assets/img/enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))

        self.rect = self.image.get_rect(x = start_x,  y = start_y)

        self.speed = ENEMY_SPEED * speed_mult
    
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
        surface.blit(self.image, self.rect)