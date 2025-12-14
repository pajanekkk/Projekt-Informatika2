"""
Slouzi k zakladnim funkcim, ktere umoznuji aby se hra spustila, bezela dobre, napr. vytvoreni okna atd...
"""
import pygame
import random
from src.player import *
from src.settings import *
from src.bullet import *
from src.enemy import *

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
        self._spawn_start_enemies()

        self.wave_timer = 0.0

        self.score = 0
        self.lives = PLAYER_LIVES
        # false - normalni hra
        # true - konec
        self.game_over = False
        
        self.paused = False

        self.running = True

    def run(self) -> None:
        while self.running:
            dt = self._get_delta_time()
            
            self._handle_events(dt)
            
            if not self.game_over and not self.paused:
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

            # pauza
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not self.game_over:
                    self.paused = not self.paused
        
            # strelba
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if pressed_keys[pygame.K_SPACE]:
                    new_bullet = self.player.shoot()
                    self.bullets.append(new_bullet)
        # restart    
        if self.game_over:
            if pressed_keys[pygame.K_r]:
                self._restart_game()

    def _restart_game(self):
        """
        funkce pro restart hry
        """
        self.bullets.clear()
        self.enemies.clear()

        self.lives = PLAYER_LIVES
        self.score = 0

        self.game_over = False

    def _spawn_start_enemies(self) -> None:
        """
        spawne pocatecni nepratele
        """
        for _ in range(START_ENEMY):
            x = random.randint(ENEMY_WIDTH // 2, WINDOW_WIDTH - WINDOW_WIDTH // 2)
            y = random.randint(-300, -ENEMY_HEIGHT)
            self.enemies.append(Enemy(x, y))


    def _handle_waves(self, dt: float) -> None:
        """
        pridava nepratele po vlnach
        """
        self.wave_timer += dt

        if self.wave_timer >= WAVE_INTERVAL:
            self.wave_timer = 0.0
        
            for _ in range(WAVE_ENEMY):
                x = random.randint(ENEMY_WIDTH // 2, WINDOW_WIDTH - ENEMY_WIDTH // 2)
                y = -ENEMY_HEIGHT
                self.enemies.append(Enemy(x, y))

    def _check_collisions(self) -> None:
        """
        checkuje kolize, tzn. jestli se enemy a bullet stretnou atd,
        if yes -> tak je smaze, atd
        """
        # tady se budou pridavat entity, ktere budou smazany
        bullets_to_remove = []
        enemies_to_remove = []
        

        for bullet in self.bullets:
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect):
                    bullets_to_remove.append(bullet)
                    enemies_to_remove.append(enemy)
                    self.score += 1
        
        # odstrani trefene objekty
        self.bullets = [b for b in self.bullets if b not in bullets_to_remove]
        self.enemies = [e for e in self.enemies if e not in enemies_to_remove]

        # pole pro nepratele, kteri zasahnou hrace
        enemies_hit_player = []
        for enemy in self.enemies:
            if enemy.rect.colliderect(self.player.rect):
                enemies_hit_player.append(enemy)
                self.lives -= 1

        # smaze enemaky, co narazi do playera
        self.enemies = [e for e in self.enemies if e not in enemies_hit_player]

        # game over - zatim jenom zavre program
        # TODO: bude to vypadat lip, pinky promise :((
        if self.lives <= 0:
            self.game_over = True

    def _update(self, dt: float) -> None:

        self.player.update(dt)

        # update strel
        for bullet in self.bullets:
            bullet.update(dt)

        # smazat strely mimo okno
        self.bullets = [b for b in self.bullets if not b.is_offscreen()]

        # update enemies
        for enemy in self.enemies:
            enemy.update(dt)
        
        # spawn novych enemies
        self._handle_waves(dt)


        # kolize
        self._check_collisions()

        # mazani enemies, kteri jsou mimo hraci okno
        self.enemies = [e for e in self.enemies if not e.is_offscreen()]



    def _draw(self) -> None:
        """
        vykreslovani na obrazovku
        """
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)

        for bullet in self.bullets:
            bullet.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # text na skore a zivoty
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(f"Skóre: {self.score} Zivoty: {self.lives}", True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 10))
        
        # vykresleni prohry
        if self.game_over:
            # go - game over, r - restart
            font_go = pygame.font.SysFont(None, 48)
            font_r = pygame.font.SysFont(None, 28)

            text_go = font_go.render("PROHRÁL SI!", True, (255, 0, 0))
            text_r = font_r.render("ZMÁČKNI 'R' PRO RESTART HRY!", True, (255, 255, 255))

            rect_go = text_go.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
            rect_r = text_r.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))

            self.screen.blit(text_go, rect_go)
            self.screen.blit(text_r, rect_r)
        
        # vykresleni pauzy
        if self.paused:
            font_p = pygame.font.SysFont(None, 48)

            text_p = font_p.render("HRA POZASTAVENA!", True, (255, 255, 255))
            rect_p = text_p.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

            self.screen.blit(text_p, rect_p)

        pygame.display.flip()
