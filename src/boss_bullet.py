"""
Slouzi pro funkce strileni bosse
"""
import pygame
from src.settings import *


class BossBullet:
    """
    Trida pro strelu od bosse
    """
    image = pygame.image.load("assets/img/boss_rocket.png")
    image = pygame.transform.scale(image, (15, 40))
    def __init__(self, start_x: int, start_y: int, dx: int = 0) -> None:

        self.rect = BossBullet.image.get_rect(centerx = start_x, y = start_y)
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
        surface.blit(BossBullet.image, self.rect)