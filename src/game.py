"""
Slouzi k funkcim, ktere umoznuji aby se hra spustila, bezela dobre, napr. vytvoreni okna, vizualu atd...
"""
import pygame
import random
from src.player import *
from src.settings import *
from src.bullet import *
from src.enemy import *
from src.boss import *
from src.boss_bullet import *

class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Space defender")

        self.clock = pygame.time.Clock()

        start_x = WINDOW_WIDTH // 2
        start_y = WINDOW_HEIGHT - 60
        self.player = Player(start_x, start_y)
        self.boss = None

        # do techto poli se budou nahravet vytvorene "entity"
        self.bullets = []
        self.enemies = []
        self.boss_bullets = []

        self.enemy_speed = ENEMY_SPEED

        self.enemies_in_wave = 2
        self.wave_active = True
        self.curr_wave = 29
        self.wave_pause = False
        self.wave_p_timer = 0.0
        self.wave_p_dur = 3.0

        self.score = 0
        self.lives = PLAYER_LIVES

        # false - normalni hra
        # true - konec, pauza, vitezstvi
        self.game_over = False
        
        self.paused = False

        self.victory = False

        self.running = True
        self._start_wave()

    def run(self) -> None:
        while self.running:
            dt = self._get_delta_time()
            
            self._handle_events(dt)
            
            if not self.game_over and not self.paused and not self.victory:
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
            if pressed_keys[pygame.K_ESCAPE]:
                if not self.game_over:
                    self.paused = not self.paused
        
            if pressed_keys[pygame.K_SPACE]: 
                if not self.game_over and not self.paused and not self.victory:
                    new_bullet = self.player.shoot()
                    self.bullets.append(new_bullet)
        # restart    
        if self.game_over or self.victory or self.paused:
            if pressed_keys[pygame.K_r]:
                self._restart_game()

    def _restart_game(self) -> None:
        """
        funkce pro restart hry
        """
        self.bullets.clear()
        self.enemies.clear()

        self.lives = PLAYER_LIVES
        self.score = 0
        self.curr_wave = 0
        self.enemies_in_wave = 2

        self.game_over = False
        self.wave_pause = False
        self.wave_p_timer = 0.0
        self.victory = False
        self._start_wave()


    def _start_wave(self) -> None:
        """
        spawne novou vlnu
        """
        self.wave_active = True
        for _ in range(self.enemies_in_wave):
            x = random.randint(ENEMY_WIDTH // 2, WINDOW_WIDTH - ENEMY_WIDTH // 2)
            y = random.randint(-300, -ENEMY_HEIGHT)
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
                    self.score += 100
        
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

        # game over
        if self.lives <= 0:
            self.game_over = True
        # strela hrace vs boss
        if self.boss:
            for bullet in self.bullets[:]:
                if self.boss and bullet.rect.colliderect(self.boss.rect):
                    self.bullets.remove(bullet)
                    self.boss.take_dmg(1)

                if self.boss and self.boss.hp <= 0:
                    self.boss = None
                    self.victory = True
            for b in self.boss_bullets[:]:
                if b.rect.colliderect(self.player.rect):
                    self.boss_bullets.remove(b)
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True


    def _update(self, dt: float) -> None:
        """
        update funkce(at se to muze hybat po obrazovce atd.)
        """
        if not self.game_over and not self.paused and not self.victory:
            self.player.update(dt)
            # update strel
            for bullet in self.bullets:
                bullet.update(dt)

            # update enemies
            for enemy in self.enemies:
                enemy.update(dt)

        # kolize
        self._check_collisions()
        # smazat strely mimo okno
        self.bullets = [b for b in self.bullets if not b.is_offscreen()]    

        remaining_enemies = []
        for enemy in self.enemies:
            if enemy.is_offscreen():
                self.score -= 50
            else:
                remaining_enemies.append(enemy)
        self.enemies = remaining_enemies
        
        # dalsi vlna
        if self.wave_active and len(self.enemies) == 0:
            self.wave_active = False
            self.wave_pause = True
            self.wave_p_timer = 0.0

        # mezipauza u vln
        if self.wave_pause:
            self.wave_p_timer += dt

            if self.wave_p_timer >= self.wave_p_dur:
                self.wave_pause = False
                
                if self.curr_wave == MAX_WAVES:
                    self.boss = Boss()
                    self.wave_active = False
                    self.wave_pause = False
                    return

                                
                self.curr_wave += 1
                # zvyseni obtiznosti
                self.enemies_in_wave += 1

                self._start_wave()
        if self.boss:
            self.boss.update(dt)
        
        if self.boss and self.boss.can_boss_shoot():
            bx = self.boss.rect.centerx
            by = self.boss.rect.bottom
            self.boss_bullets.append(BossBullet(bx, by))
        
        for b in self.boss_bullets:
            b.update(dt)
        self.boss_bullets = [b for b in self.boss_bullets if not b.is_offscreen()]

    def _draw_game_status(self, m_text, b_text, color) -> None:
        """
        funkce pro vykresleni stavu hry(vyhra, prohra, pauza)
        
        :param m_text: hlavni text
        :param b_text: podtext
        :param color: barva textu
        """
        font_m = pygame.font.SysFont(None, 48)
        font_b = pygame.font.SysFont(None, 28)

        text1 = font_m.render(m_text, True, color)
        text2 = font_b.render(b_text, True, (255, 255, 255))

        rect1 = text1.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
        rect2 = text2.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))

        self.screen.blit(text1, rect1)
        self.screen.blit(text2, rect2)


    def _draw(self) -> None:
        """
        vykreslovani na obrazovku
        """
        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)

        if not self.game_over and not self.paused and not self.victory:
            for bullet in self.bullets:
                bullet.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        if self.boss:
            self.boss.draw(self.screen)
        
        if self.boss and not self.game_over and not self.paused and not self.victory:
            for b in self.boss_bullets:
                b.draw(self.screen)

        
        # text pro statistiky
        font = pygame.font.SysFont(None, 24)

        text_scoliv = font.render(f"Skóre: {self.score} Životy: {self.lives}", True, (255, 255, 255))
        text_wave = font.render(f"Vlna: {self.curr_wave}", True, (255, 255, 255))

        self.screen.blit(text_scoliv, (10, 10))
        self.screen.blit(text_wave, (10, 30))


        # vykresleni mezipauzy u vln
        if self.wave_pause and not self.curr_wave == 0:
            self._draw_game_status(f"Vlna {self.curr_wave} dokončena", None, (0, 255, 255))
        # vykresleni vyhry
        if self.victory:
            self._draw_game_status("VYHRÁL SI!", "R pro restart", (255, 0, 0))
        # vykresleni prohry
        if self.game_over:
            self._draw_game_status("PROHRÁL SI!", "R pro restart", (255, 0, 0))
        # vykresleni pauzy
        if self.paused:
            self._draw_game_status("HRA POZASTAVENA!", "R pro restart", (255, 0, 0))

        pygame.display.flip()
