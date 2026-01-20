"""
Slouzi k implementaci funkci pro tridu hrace
"""
import pygame
from src.settings import *
from src.bullet import Bullet


class Player:
    """
    Trida pro hrace
    """
    def __init__(self) -> None:
        
        self.image = pygame.image.load("assets/img/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))

        self.rect = self.image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 80))
        # rychlost v ose x
        self.speed = PLAYER_SPEED
    
    def handle_input(self, pressed_keys, dt: float) -> None:
        """
        Zpracovani pohybu
        """
        dx = 0.0 # jakoby osa x
        dy = 0.0 # osa y

        # posun doleva
        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
            dx -= self.speed * dt

        # posun doprava
        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            dx += self.speed * dt
        
        # posune dolu
        if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
            dy += self.speed * dt
        
        # posun nahoru
        if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
            dy -= self.speed * dt
        
        # posunuti hrace po ose x a y
        self.rect.x += int(dx)
        self.rect.y += int(dy)

        # osetreni hrace mimo obrazovku
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT


    def update(self, dt: float) -> None:
        # TODO ?? to asi nepotrebuju ze??? uvaha pls
        pass

    def draw(self, surface: pygame.Surface) -> None:
        """
        Vykresleni hrace na obrazovku
        """
        surface.blit(self.image, self.rect)
    
    def shoot(self) -> Bullet:
        bullet_x = self.rect.centerx
        bullet_y = self.rect.top
        return Bullet(bullet_x, bullet_y)
