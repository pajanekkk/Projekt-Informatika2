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

        self.flash_timer = 0.0
        self.flash_t_dur = 0.15 # sekundy

        self.score = 0
        self.lives = PLAYER_LIVES

        # false - normalni hra
        # true - konec, pauza, vitezstvi
        self.game_over = False
        
        self.paused = False

        self.victory = False

        self.state = "MENU"
        self.player_name = ""

        self.running = True
        self._start_wave()

    def run(self) -> None:
        while self.running:
            dt = self._get_delta_time()
            
            self._handle_events(dt)
            if self.state == "PLAYING":
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

        # TOHLE POUZE PRO HRACE!!!!!!!!!!!!!!!!
        pressed_keys = pygame.key.get_pressed()
        self.player.handle_input(pressed_keys, dt)
        #######################################
        for event in pygame.event.get():
            # exit
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
            # prechod z menu
                if self.state == "MENU":
                    if event.key == pygame.K_RETURN:
                        self.state = "NAME_INPUT"
                        self.player_name = ""
                
                if self.state == "NAME_INPUT":
                    if event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        if len(self.player_name) > 0:
                            self._start_game()
                    else:
                        if len(self.player_name) < 8 and event.unicode.isalnum():
                            self.player_name += event.unicode.upper()
                # pauza
                if event.key == pygame.K_ESCAPE:
                    if not self.game_over:
                        self.paused = not self.paused
            
                if event.key == pygame.K_SPACE: 
                    if not self.game_over and not self.paused and not self.victory:
                        new_bullet = self.player.shoot()
                        self.bullets.append(new_bullet)
                
                if event.key == pygame.K_RETURN:
                    if self.state == "GAME_OVER" or self.state == "VICTORY":
                        self.state = "MENU"
            # restart    
            if self.game_over or self.victory or self.paused:
                if event.key == pygame.K_r:
                    self._restart_game()

    def _restart_game(self) -> None:
        """
        funkce pro restart hry
        """
        self.bullets.clear()
        self.enemies.clear()

        self.lives = PLAYER_LIVES
        self.score = 0
        self.curr_wave = 29
        self.enemies_in_wave = 2

        self.game_over = False
        self.wave_pause = False
        self.wave_p_timer = 0.0
        self.victory = False
        self.curr_wave = self.curr_wave + 1
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

    def _start_game(self) -> None:
        """
        spusti hru tzv. prechod z menu do akce
        """
        self.state = "PLAYING"
        self._restart_game()

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
                self.flash_timer = self.flash_t_dur


        # smaze enemaky, co narazi do playera
        self.enemies = [e for e in self.enemies if e not in enemies_hit_player]

        # game over
        if self.lives <= 0:
            self.state = "GAME_OVER"
        # strela hrace vs boss
        if self.boss:
            for bullet in self.bullets[:]:
                if self.boss and bullet.rect.colliderect(self.boss.rect):
                    self.bullets.remove(bullet)
                    self.boss.take_dmg(1)

                if self.boss and self.boss.hp <= 0:
                    self.boss = None
                    self.state = "VICTORY"
            for b in self.boss_bullets[:]:
                if b.rect.colliderect(self.player.rect):
                    self.boss_bullets.remove(b)
                    self.lives -= 1
                    self.flash_timer = self.flash_t_dur
                    if self.lives <= 0:
                        self.state = "GAME_OVER"
                        self.boss = None


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
            self.boss_bullets.append(BossBullet(bx, by, 0))
            self.boss_bullets.append(BossBullet(bx, by, -150))
            self.boss_bullets.append(BossBullet(bx, by, 150))
        
        for b in self.boss_bullets:
            b.update(dt)
        self.boss_bullets = [b for b in self.boss_bullets if not b.is_offscreen()]

        if self.flash_timer > 0:
            self.flash_timer -= dt

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

    def _draw_endscreen(self, state):
        """
        funkce pro vykreslení konecne obrazovyk - game over/vyhra
        :param state: stav hry
        """
        self.screen.fill((255, 255, 255))

        # b - big text, m - maly text, s - stredni text
        font_b = pygame.font.SysFont(None, 48)
        font_s = pygame.font.SysFont(None, 36)
        font_m = pygame.font.SysFont(None, 28)

        title_text = "PROHRÁL SI" if self.state == "GAME_OVER" else "VYHRÁL SI!"
        if self.state == "GAME_OVER":
            subtext = "Bohužel si zemřel ve svém letounu při obraně tvého města..."
        else:
            subtext = ("Povedlo se ti odrazit nepřátelský útok a tím předejít katastrofě...")
        
        title = font_b.render(title_text, True, (0, 0, 0))
        sub = font_s.render(subtext, True, (0, 0, 0))
        name = font_m.render(f"Jméno: {self.player_name}", True, (0, 0, 0))
        score = font_m.render(f"Skóre: {self.score}", True, (0, 0, 0))
        ufncn = font_m.render("ENTER pro návrat do menu", True, (80, 80, 80))  # ufncn - uz fakt nevim co napsat -> symbolizuje me utrpeni pri psani teto hry

        self.screen.blit(title, title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40)))
        self.screen.blit(sub, sub.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)))
        self.screen.blit(name, name.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30)))
        self.screen.blit(score, score.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 70)))
        self.screen.blit(ufncn, ufncn.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 110)))

        pygame.display.flip()


    def _draw(self) -> None:
        """
        vykreslovani na obrazovku
        """
        self.screen.fill((0, 0, 0))
        if self.state == "MENU":
            self._draw_game_status("NAZEV HRY", "Zmackni ENTER pro zahájení hry!", (255, 255, 255))

            pygame.display.flip()
            return

        if self.state == "NAME_INPUT":
            self._draw_game_status("ZADEJ JMENO! ENTER PRO POTVRZENI...", self.player_name + "_", (155, 155, 0))
            pygame.display.flip()
            return

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
            self._draw_game_status(f"Vlna {self.curr_wave} dokončena", None, (0, 0, 255))
        # vykresleni pauzy
        if self.paused:
            self._draw_game_status("HRA POZASTAVENA!", "R pro restart / Q pro ukončení", (255, 0, 0))

        if self.state == "VICTORY" or self.state == "GAME_OVER":
            self._draw_endscreen(self.state)

        # tohle je jakoby probliknuti
        if self.flash_timer > 0 and self.state == "PLAYING":
            flash_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            flash_surf.set_alpha(180) # semi-transparentni
            flash_surf.fill((255, 255, 255)) # bila
            self.screen.blit(flash_surf, (0, 0))

        pygame.display.flip()
