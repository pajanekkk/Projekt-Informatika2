"""
Slouzi pro funkce strileni bosse
"""
import pygame
from src.settings import *


class BossBullet:
    def __init__(self, x: int, y: int) -> None:
        self.rect = pygame.Rect(x - 6, y, 12, 18)
        self.speed = 300

    def update(self, dt: float):
        self.rect.y += int(self.speed * dt)
    
    def is_offscreen(self) -> bool:
        return self.rect.top > WINDOW_HEIGHT
    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, BOSS_BULL_COL, self.rect)