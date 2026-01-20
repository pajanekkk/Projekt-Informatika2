"""
Slouzi pro funkcnost bosse
"""
import pygame
import random
from src.settings import *

class Boss:
    """
    Trida pro bosse
    """
    def __init__(self) -> None:
        self.image = pygame.image.load("assets/img/boss.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (170, 100))
        self.image = pygame.transform.flip(self.image, False, True)


        self.rect = self.image.get_rect(center=(WINDOW_WIDTH // 2, 100))

        self.speed = BOSS_SPEED
        self.dir = 1 # 1 = doprava, -1 = doleva

        self.hp = BOSS_HP

        self.shoot_timer = 0.0
        self.shoot_cooldown = 1.5 # sekundy

        self.target_x = self.rect.x
        self.target_y = self.rect.y
        self._pick_new_target()

    def update(self, dt: float):
        """
        pohyb bosse, pokus o jednoduchou AI
        """
        dx = self.target_x - self.rect.x
        dy = self.target_y - self.rect.y

        dist = (dx ** 2 + dy ** 2) ** 0.5

        if dist < 5:
            self._pick_new_target()
            return
        
        dx /= dist
        dy /= dist

        self.rect.x += int(dx * self.speed * dt)
        self.rect.y += int(dy * self.speed * dt)

        self.shoot_timer += dt

    def can_boss_shoot(self):
        """
        muze boss strilet? ano, pokud timer presahne/rovna se cooldownu
        """
        if self.shoot_timer >= self.shoot_cooldown:
            self.shoot_timer = 0.0
            return True
        return False
    
    def _pick_new_target(self):
        """
        vymezuje cast okna kde muze litat (v podstate "cilove body" slouzici pro bosse kam letet)
        """
        import random
        self.target_x = random.randint(0, WINDOW_WIDTH - self.rect.width)
        self.target_y = random.randint(0, WINDOW_HEIGHT // 2)

    def take_dmg(self, amount: int):
        """
        bossovi ubira zivoty
        """
        self.hp -= amount
    
    def draw(self, surface):
        """
        vykresleni bosse
        """
        surface.blit(self.image, self.rect)

        bar_width = BOSS_WIDTH
        bar_height = 8
        hp_ratio = self.hp / BOSS_HP

        pygame.draw.rect(surface, (255, 0, 0), (self.rect.x, self.rect.y - 12, bar_width, bar_height))

        pygame.draw.rect(surface, (0, 255, 0), (self.rect.x, self.rect.y - 12, int(bar_width * hp_ratio), bar_height))