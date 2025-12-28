"""
Slouzi pro funkcnost bosse
"""
import pygame
import random
from src.settings import *




class Boss:
    def __init__(self) -> None:

        self.rect = pygame.Rect((WINDOW_WIDTH - BOSS_WIDTH) // 2, 40, BOSS_WIDTH, BOSS_HEIGHT)

        self.speed = BOSS_SPEED
        self.dir = 1 # 1 = doprava, -1 = doleva

        self.hp = BOSS_HP

        self.shoot_timer = 0.0
        self.shoot_cooldown = 1.5 # sekundy

    def update(self, dt: float):
        """
        pohyb bosse ze strany na stranu (zatim?)
        """
        self.rect.x += int(self.speed * self.dir * dt)

        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.dir *= -1

        self.shoot_timer += dt
    
    def can_boss_shoot(self):
        """
        muze boss strilet? ano, pokud timer presahne/rovna se cooldownu
        """
        if self.shoot_timer >= self.shoot_cooldown:
            self.shoot_timer = 0.0
            return True
        return False
    
    def take_dmg(self, amount: int):
        """
        bossovi ubira zivoty
        """
        self.hp -= amount
    
    def draw(self, surface):
        pygame.draw.rect(surface, BOSS_COLOR, self.rect)

        bar_width = BOSS_WIDTH
        bar_height = 8
        hp_ratio = self.hp / BOSS_HP

        pygame.draw.rect(surface, (255, 0, 0), (self.rect.x, self.rect.y - 12, bar_width, bar_height))

        pygame.draw.rect(surface, (0, 255, 0), (self.rect.x, self.rect.y - 12, int(bar_width * hp_ratio), bar_height))