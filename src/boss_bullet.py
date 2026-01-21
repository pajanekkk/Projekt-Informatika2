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
    
    image_R = pygame.transform.rotate(image, -45)
    
    image_L = pygame.transform.rotate(image, 45)
    
    def __init__(self, start_x: int, start_y: int, dx: int = 0, dy: int = 0) -> None:

        self.rect = BossBullet.image.get_rect(centerx = start_x, y = start_y)
        self.rect_R = BossBullet.image_R.get_rect(centerx = start_x, y = start_y)
        self.rect_L = BossBullet.image_L.get_rect(centerx = start_x, y = start_y)
        self.speed_y = 300 + dy
        self.speed_x = dx
        
        # typ rakety podle dx
        if dx == 0:
            self.bullet_type = "center"
        elif dx > 0:
            self.bullet_type = "left"
        else:
            self.bullet_type = "right"


    def update(self, dt: float):
        """
        update funkce
        """
        self.rect.y += int(self.speed_y * dt)
        self.rect.x += int(self.speed_x * dt)
        
        self.rect_R.y += int(self.speed_y * dt)
        self.rect_R.x += int(self.speed_x * dt)
        
        self.rect_L.y += int(self.speed_y * dt)
        self.rect_L.x += int(self.speed_x * dt)

    def is_offscreen(self) -> bool:
        """
        kontrola if mimo obrazovku
        """
        if self.rect.top > WINDOW_HEIGHT and self.rect_R.top > WINDOW_HEIGHT and self.rect_L.top > WINDOW_HEIGHT:
            return True
        return False
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        vykresleni strely bosse
        """
        if self.bullet_type == "center":
            surface.blit(BossBullet.image, self.rect)
        elif self.bullet_type == "left":
            surface.blit(BossBullet.image_L, self.rect_L)
        elif self.bullet_type == "right":
            surface.blit(BossBullet.image_R, self.rect_R)