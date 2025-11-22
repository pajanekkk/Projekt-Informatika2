"""
Slouzi k zakladnim funkcim, ktere umoznuji aby se hra spustila, bezela dobre, napr. vytvoreni okna atd...
"""
import pygame
import random
from src.player import *
from src.settings import *
from src.bullet import *
class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Space defender")

        self.clock = pygame.time.Clock()

        start_x = WINDOW_WIDTH // 2
        start_y = WINDOW_HEIGHT - 60
        self.player = Player(start_x, start_y)

        # do techto poli se budou nahravet vytvorene "entity"
        self.bullets = []
        self.enemies = []

        self.score = 0
        self.lives = PLAYER_LIVES

        self.running = True

    def run(self) -> None:
        while self.running:
            dt = self._get_delta_time()
            self._handle_events(dt)
            self._update(dt)
            self._draw()

    def _get_delta_time(self) -> float:
        """
        funkce aby rychlost nepratel + hrace byla konstantne stejna a nebyla zavisla na FPS
        napr. pohyb 20 pixelu za sekundu a ne 20 pixelu za snimek
        """
        dt_ms = self.clock.tick(FPS)
        dt = dt_ms / 1000.0
        return dt
    
    def _handle_events(self, dt) -> None:
        """
        funkce pro zpracovani eventu, jako je quit, nebo zmacknuti klaves pro strileni atd.
        """
        pressed_keys = pygame.key.get_pressed()
        self.player.handle_input(pressed_keys, dt)
        
        for event in pygame.event.get():
            # exit
            if event.type == pygame.QUIT:
                self.running = False
            
            # strelba
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if pressed_keys[pygame.K_SPACE]:
                    new_bullet = self.player.shoot()
                    self.bullets.append(new_bullet)
        
            

    
    def _update(self, dt: float) -> None:
        self.player.update(dt)

        # update strel
        for bullet in self.bullets:
            bullet.update(dt)

        # smazat strely mimo okno
        self.bullets = [b for b in self.bullets if not b.is_offscreen()]

        # tady pak budou enemies - TODO


    def _draw(self) -> None:
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)

        for bullet in self.bullets:
            bullet.draw(self.screen)

        # TODO - skore, zivoty
        
        pygame.display.flip()
