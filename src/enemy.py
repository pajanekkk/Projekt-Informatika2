"""
Slouzi k implementaci tridy pro nepritele
"""

import pygame
import random
from src.settings import *



class Enemy:
    def __init__(self, start_x: float, start_y: float) -> None:
        
        self.image = pygame.image.load("assets/enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))

        self.rect = self.image.get_rect(x=random.randint(0, WINDOW_WIDTH - 40), y = -40)

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
        surface.blit(self.image, self.rect)