import pygame
from src.settings import *
from src.bullet import Bullet

PLAYER_COLOR = (0, 255, 0)

class Player:
    def __init__(self, start_x: float, start_y: float) -> None:
        """
        start_x, start_y - pocatecni pozice
        """
        self.rect = pygame.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.rect.centerx = int(start_x)
        self.rect.centery = int(start_y)

        # rychlost v ose x
        self.speed = PLAYER_SPEED
    
    def handle_input(self, pressed_keys, dt: float) -> None:
        """
        Zpracovani pohybu
        """
        dx = 0.0 # jakoby osa x

        # posun doleva
        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
            dx -= self.speed * dt

        # posun doprava
        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            dx += self.speed * dt
        
        # posunuti hrace po ose x
        self.rect.x += int(dx)

        # osetreni hrace mimo obrazovku
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH

    def update(self, dt: float) -> None:
        # TODO
        pass

    def draw(self, surface: pygame.Surface) -> None:
        """
        Vykresleni hrace na obrazovku
        """
        pygame.draw.rect(surface, PLAYER_COLOR, self.rect)
    
    def shoot(self) -> Bullet:
        bullet_x = self.rect.centerx
        bullet_y = self.rect.top
        return Bullet(bullet_x, bullet_y)
