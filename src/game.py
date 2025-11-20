# Game.py slouzi k zakladnim funkcim, ktere umoznuji aby se hra spustila, bezela dobre, napr. vytvoreni okna atd...

import pygame
from src.player import *
from src.settings import *

class Game:
    def __init__(self):
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

    def run(self):
        while self.running:
            dt = self._get_delta_time()
            self._handle_events(dt)

            self._draw()

    def _get_delta_time(self):
        """
        funkce aby rychlost nepratel + hrace byla konstantne stejna a nebyla zavisla na FPS
        napr. pohyb 20 pixelu za sekundu a ne 20 pixelu za snimek
        """
        dt_ms = self.clock.tick(FPS)
        dt = dt_ms / 1000.0
        return dt
    
    def _handle_events(self, dt):
        """
        funkce pro zpracovani eventu, jako je quit, nebo zmacknuti klaves pro strileni atd.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        pressed_keys = pygame.key.get_pressed()
        self.player.handle_input(pressed_keys, dt)

    def _draw(self):
        self.screen.fill((255, 255, 255))

        self.player.draw(self.screen)
        pygame.display.flip()