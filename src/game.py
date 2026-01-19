"""
Slouzi k funkcim, ktere umoznuji aby se hra spustila, bezela dobre, napr. vytvoreni okna, vizualu atd...
"""
import pygame
import random
import json
import os

from src.player import Player
from src.settings import *
from src.enemy import Enemy
from src.boss import Boss
from src.boss_bullet import BossBullet
from src.explosion import Explosion

class Game:
    def __init__(self) -> None:
        pygame.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("ÚTOK DRONŮ")

        self.clock = pygame.time.Clock()

        """ self.bg = pygame.image.load("assets/img/bg.png").convert()
        self.bg = pygame.transform.scale(self.bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.bg_y = 0 # osa y v podstate
        self.bg_speed = 40 # px za sekundu """
        
        self.font_title = pygame.font.Font("assets/fonts/Oxanium-Bold.ttf",  48)
        self.font_menu = pygame.font.Font("assets/fonts/Oxanium-Regular.ttf",  36)
        self.basic_text = pygame.font.Font("assets/fonts/Oxanium-Regular.ttf",  24)
        self.font_hint = pygame.font.Font("assets/fonts/Oxanium-Light.ttf",  28)
    
        self.player = Player()
        self.boss = None
        self.highscores = self._load_highscores()

        # do techto poli se budou nahravet vytvorene "entity"
        self.bullets = []
        self.enemies = []
        self.boss_bullets = []

        self.enemy_speed = ENEMY_SPEED

        self.enemies_in_wave = 2
        self.wave_active = True
        self.curr_wave = 0
        self.wave_pause = False
        self.wave_p_timer = 0.0
        self.wave_p_dur = 3.0

        self.spawn_queue = []
        self.spawn_q_timer = 0.0
        self.spawn_delay = 1


        self.flash_timer = 0.0
        self.flash_t_dur = 0.15 # sekundy

        self.boss_dying = False
        self.boss_death_timer = 0.0

        self.score = 0
        self.lives = PLAYER_LIVES

        # false - normalni hra
        # true - konec, pauza, vitezstvi
        self.game_over = False
        
        self.paused = False

        self.victory = False

        self.explosions = []

        self.shoot_sound = pygame.mixer.Sound("assets/sounds/shoot.wav")
        self.boss_hit_player_sound = pygame.mixer.Sound("assets/sounds/boss_hit-player.wav")
        self.collision_sound = pygame.mixer.Sound("assets/sounds/collision.wav")
        self.menu_song = pygame.mixer.Sound("assets/sounds/menu.wav")
        self.play_song = pygame.mixer.Sound("assets/sounds/playing1.wav")
        self.losing_sound = pygame.mixer.Sound("assets/sounds/losing.wav")
        self.explosion_boss_sound = pygame.mixer.Sound("assets/sounds/explosion_boss_sound.wav")
        
        self.curr_music = None

        self.state = "MENU"
        self.player_name = ""

        self.menu_items = ["SPUSTIT HRU", "NASTAVENÍ", "NEJVYŠŠÍ SKÓRE", "UKONČIT"]
        self.menu_index = 0
        
        self.settings_index = 0
        
        self.wave_opts = [15, 25, 35]
        self.wave_opt_index = 1 # defaultne 15

        self.enemy_speed_opts = [
            ("POMALÝ", 0.7),
            ("NORMALNÍ", 1.0),
            ("RYCHLE", 1.3),
        ]
        self.enemy_speed_index = 1 # defaultne na NORMAL

        self.music_vol = 0.6
        self.sfx_vol = 0.8
        self.vol_step = 0.1

        self._apply_volume()

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
                    self._play_music(self.menu_song, True)
                    if event.key == pygame.K_UP:
                        self.menu_index = (self.menu_index - 1) % len(self.menu_items)
                    elif event.key == pygame.K_DOWN:
                        self.menu_index = (self.menu_index + 1) % len(self.menu_items)
                    elif event.key == pygame.K_RETURN:
                        choice = self.menu_items[self.menu_index]
                        if choice == "SPUSTIT HRU":
                            self.state = "NAME_INPUT"
                        elif choice == "NASTAVENÍ":
                            self.state = "SETTINGS"
                        elif choice == "NEJVYŠŠÍ SKÓRE":
                            self.state = "HIGHSCORE"
                        elif choice == "UKONČIT":
                            self.running = False
                
                if self.state == "SETTINGS":
                    if event.key == pygame.K_UP:
                        self.settings_index = (self.settings_index - 1) % 4
                    if event.key == pygame.K_DOWN:
                        self.settings_index = (self.settings_index + 1) % 4

                    if event.key == pygame.K_LEFT:
                        if self.settings_index == 0:
                            self.wave_opt_index = (self.wave_opt_index - 1) % len(self.wave_opts)
                        if self.settings_index == 1:
                            self.enemy_speed_index = (self.enemy_speed_index - 1) % len(self.enemy_speed_opts)
                        if self.settings_index == 2:
                            self.sfx_vol = max(0.0, self.sfx_vol - self.vol_step)
                            self._apply_volume()
                        if self.settings_index == 3:
                            self.music_vol = max(0.0, self.music_vol - self.vol_step)
                            self._apply_volume()

                    elif event.key == pygame.K_RIGHT:
                        if self.settings_index == 0:
                            self.wave_opt_index = (self.wave_opt_index + 1) % len(self.wave_opts)
                        if self.settings_index == 1:
                            self.enemy_speed_index = (self.enemy_speed_index + 1) % len(self.enemy_speed_opts)
                        if self.settings_index == 2:
                            self.sfx_vol = min(1.0, self.sfx_vol + self.vol_step)
                            self._apply_volume()
                        if self.settings_index == 3:
                            self.music_vol = min(1.0, self.music_vol + self.vol_step)
                            self._apply_volume()
                    
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "MENU"
                # psani jmena
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
                if event.key == pygame.K_p:
                    if not self.game_over and self.state == "PLAYING":
                        self.paused = not self.paused
                # strelba
                if event.key == pygame.K_SPACE: 
                    if not self.game_over and not self.paused and not self.victory:
                        new_bullet = self.player.shoot()
                        self.shoot_sound.play()
                        self.bullets.append(new_bullet)
                # navrat do menu
                if event.key == pygame.K_ESCAPE:
                    if self.state == "GAME_OVER" or self.state == "VICTORY" or self.state == "HIGHSCORE":
                        self.state = "MENU"
                # zebricek
                if event.key == pygame.K_h:
                    if self.state == "VICTORY" or self.state == "MENU" or self.state == "GAME_OVER":
                        self.state = "HIGHSCORE"
                if event.key == pygame.K_q:
                    if self.paused:
                        self.running = False
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
        self.curr_wave = 0
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
        self.spawn_queue.clear()
        
        padding = 20
        enemy_w = ENEMY_WIDTH
        
        cols = WINDOW_WIDTH // (enemy_w + padding)

        used_cols = []

        for _ in range(self.enemies_in_wave):
            # vybere nahodny volny "slot"
            col = random.randint(0, cols - 1)
            while col in used_cols:
                col = random.randint(0, cols - 1)
            used_cols.append(col)

            x = col * (enemy_w + padding) + padding
            y = random.randint(-200, -50)
            
            self.spawn_queue.append((x, y))

    def _start_game(self) -> None:
        """
        spusti hru tzv. prechod z menu do akce
        """
        global MAX_WAVES
        MAX_WAVES = self.wave_opts[self.wave_opt_index]
        self.enemy_speed_mult = self.enemy_speed_opts[self.enemy_speed_index][1]


        self._play_music(self.play_song, True)
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
                    self.explosions.append(Explosion(enemy.rect.centerx, enemy.rect.centery))
                    self.score += 100
        
        # odstrani trefene objekty
        self.bullets = [b for b in self.bullets if b not in bullets_to_remove]
        self.enemies = [e for e in self.enemies if e not in enemies_to_remove]

        # pole pro nepratele, kteri zasahnou hrace
        enemies_hit_player = []
        for enemy in self.enemies:
            if enemy.rect.colliderect(self.player.rect):
                enemies_hit_player.append(enemy)
                self.collision_sound.play()
                self.lives -= 1
                self.flash_timer = self.flash_t_dur


        # smaze enemaky, co narazi do playera
        self.enemies = [e for e in self.enemies if e not in enemies_hit_player]

        # game over
        if self.lives <= 0:
            self._play_music(self.losing_sound, False)
            self.state = "GAME_OVER"
        # strela hrace vs boss
        if self.boss:
            for bullet in self.bullets[:]:
                if not self.boss_dying and bullet.rect.colliderect(self.boss.rect):
                    self.bullets.remove(bullet)
                    self.boss.take_dmg(1)

            if self.boss and self.boss.hp <= 0 and not self.boss_dying:
                self.boss_dying = True
                self.boss_death_timer = 3.0                
                self.explosions.append(Explosion(self.boss.rect.centerx, self.boss.rect.centery, is_boss=True))
                self.explosion_boss_sound.play()
                self.explosions.append(Explosion(self.boss.rect.centerx - 20, self.boss.rect.centery - 20, is_boss=True))
                self.explosions.append(Explosion(self.boss.rect.centerx + 20, self.boss.rect.centery + 20, is_boss=True))
                self._save_highscore()
                    
            for b in self.boss_bullets[:]:
                if b.rect.colliderect(self.player.rect):
                    self.boss_bullets.remove(b)
                    self.boss_hit_player_sound.play()
                    self.lives -= 1
                    self.flash_timer = self.flash_t_dur
                    if self.lives <= 0:
                        self.boss = None
                        self._play_music(self.losing_sound, False)
                        self.state = "GAME_OVER"
        
    
    def _update(self, dt: float) -> None:
        """
        update funkce(at se to muze hybat po obrazovce atd.)
        """
        
        """ self.bg_y += self.bg_speed * dt
        if self.bg_y >= WINDOW_HEIGHT:
            self.bg_y = 0 """ 
        
        if self.wave_active and self.spawn_queue:
            self.spawn_q_timer += dt

            if self.spawn_q_timer >= self.spawn_delay:
                self.spawn_q_timer = 0.0
                x, y = self.spawn_queue.pop(0)
                self.enemies.append(Enemy(x, y, self.enemy_speed_mult))


        if not self.game_over and not self.paused and not self.victory:
            self.player.update(dt)
            # update strel
            for bullet in self.bullets:
                bullet.update(dt)

            # update enemies
            for enemy in self.enemies:
                enemy.update(dt)
            
            for exp in self.explosions:
                exp.update(dt)

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
        if self.wave_active and not self.enemies and not self.spawn_queue:
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
                    self.boss_dying = False
                    self.boss_death_timer = 0.0
                    self.wave_active = False
                    self.wave_pause = False
                    return

                                
                self.curr_wave += 1
                # zvyseni obtiznosti
                self.enemies_in_wave += 1

                self._start_wave()

        
        if self.boss:
            if not self.boss_dying:
                self.boss.update(dt)
        
        if self.boss and self.boss.can_boss_shoot() and not self.boss_dying:
            bx = self.boss.rect.centerx
            by = self.boss.rect.bottom
            self.boss_bullets.append(BossBullet(bx, by, 0))
            self.boss_bullets.append(BossBullet(bx, by, -150))
            self.boss_bullets.append(BossBullet(bx, by, 150))
        
        for b in self.boss_bullets:
            b.update(dt)
        self.boss_bullets = [b for b in self.boss_bullets if not b.is_offscreen()]

        if self.boss_dying:
            self.boss_death_timer -= dt
            if self.boss_death_timer <= 0.0:
                self.boss = None
                self.boss_dying = False
                self.boss_death_timer = 0.0
                self.state = "VICTORY"
                self._save_highscore()
                self.boss_bullets.clear()

        self.explosions = [e for e in self.explosions if not e.finished]

        if self.flash_timer > 0:
            self.flash_timer -= dt

    def _draw_game_status(self, m_text, b_text, color) -> None:
        """
        funkce pro vykresleni stavu hry(vyhra, prohra, pauza)
        
        :param m_text: hlavni text
        :param b_text: podtext
        :param color: barva textu
        """

        text1 = self.font_menu.render(m_text, True, color)
        text2 = self.font_hint.render(b_text, True, (255, 255, 255))

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

        title_text = "PROHRÁL SI" if state == "GAME_OVER" else "VYHRÁL SI!"
        if state == "GAME_OVER":
            subtext = "Bohužel si zemřel ve svém letounu při obraně tvého města..."
        else:
            subtext = ("Povedlo se ti odrazit nepřátelský útok a tím předejít katastrofě...")
        
        title = font_b.render(title_text, True, (0, 0, 0))
        sub = font_s.render(subtext, True, (0, 0, 0))
        name = font_m.render(f"Jméno: {self.player_name}", True, (0, 0, 0))
        score = font_m.render(f"Skóre: {self.score}", True, (0, 0, 0))
        ufncn = font_m.render("ENTER pro návrat do menu", True, (80, 80, 80))  # ufncn - uz fakt nevim co napsat -> symbolizuje me utrpeni pri psani teto hry
        csjpnhs = font_m.render("H pro žebříček skóre", True, (80, 80, 0)) # chces se jit podivat na highscore?

        self.screen.blit(title, title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100)))
        self.screen.blit(sub, sub.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40)))
        self.screen.blit(name, name.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)))
        self.screen.blit(score, score.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40)))
        self.screen.blit(ufncn, ufncn.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80)))
        self.screen.blit(csjpnhs, csjpnhs.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 120)))

        pygame.display.flip()


    def _draw_hs(self) -> None:
        """
        funkce pro vykresleni highscore zebricku
        """
        
        self.screen.fill((255, 255, 255))

        y = WINDOW_HEIGHT // 2 - 100 # padding

        font_hs = pygame.font.SysFont(None, 48) # hs jako high score, lol
        
        title_hs = font_hs.render("NEJVYŠŠÍ SKÓRE", True, (0, 0, 0))
        title_rect = title_hs.get_rect(center=(WINDOW_WIDTH // 2, y))
        self.screen.blit(title_hs, title_rect)
        y += 60

        for i, entry in enumerate(self.highscores):
            text = font_hs.render(f"{i+1}. {entry['name']} - {entry['score']}", True, (0, 0, 0))
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y))
            self.screen.blit(text, text_rect)
            y += 50

        hint = pygame.font.SysFont(None, 24).render("ESC = ZPĚT", True, (160, 160, 160))
        self.screen.blit(hint, hint.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 60)))

        pygame.display.flip()

    def _draw(self) -> None:
        """
        vykreslovani na obrazovku
        """
        self.screen.fill((12, 14, 20))
        if self.state == "MENU":

            self.shadow_text("SPACE DEFENDER", self.font_title, (255,255,255), (100, 200, 0), (WINDOW_WIDTH//2, 100))
            y = 200
            for i, item in enumerate(self.menu_items):
                color = (255, 255, 255) if i == self.menu_index else (150, 150, 150)
                prefix = "> " if i == self.menu_index else "  "
                self.shadow_text(prefix+item, self.font_menu, (255,255,255), (255, 000, 0), (WINDOW_WIDTH//2, y))
                # text = self.font_menu.render(prefix+item, True, color)
                # self.screen.blit(text, text.get_rect(center=(WINDOW_WIDTH //2, y)))
                y += 40
            pygame.display.flip()
            return

        if self.state == "SETTINGS":
            
            
            wave_val = self.wave_opts[self.wave_opt_index]
            speed_name = self.enemy_speed_opts[self.enemy_speed_index][1]
            sfx_pct = int(self.sfx_vol * 100)
            music_pct = int(self.music_vol * 100)

            self.shadow_text("NASTAVENÍ", self.font_title, (255,255,255), (100, 200, 0), (WINDOW_WIDTH//2, 100))

            lines = [
                f"Počet vln: {wave_val}",
                f"Rychlost nepřátel: {speed_name}",
                f"Hlasitost zvuku: {sfx_pct}",
                f"Hlasitost hudby: {music_pct}"
            ]

            y = 220
            for i, line in enumerate(lines):
                color = (255, 255, 255) if i == self.settings_index else (150, 150, 150)
                self.shadow_text(line, self.font_menu, color, (255, 000, 0), (WINDOW_WIDTH//2, y))
                y += 40

            hint = self.font_hint.render("šipky pro navigaci / ESC pro návrat", True, (160,160,160))
            
            self.screen.blit(hint, hint.get_rect(center=(WINDOW_WIDTH//2, 400)))
            pygame.display.flip()
            return

        if self.state == "HIGHSCORE":
            self._draw_hs()


        if self.state == "NAME_INPUT":
            
            self._draw_game_status("ZADEJ JMENO! ENTER PRO POTVRZENI...", self.player_name + "_", (155, 155, 0))
            pygame.display.flip()
            return
        
        """ self.screen.blit(self.bg, (0, self.bg_y))
        self.screen.blit(self.bg, (0, self.bg_y - WINDOW_HEIGHT)) """

        self.player.draw(self.screen)

        if not self.game_over and not self.paused and not self.victory:
            for bullet in self.bullets:
                bullet.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        for exp in self.explosions:
            exp.draw(self.screen)
        
        if self.boss:
            self.boss.draw(self.screen)
        
        if self.boss and not self.game_over and not self.paused and not self.victory:
            for b in self.boss_bullets:
                b.draw(self.screen)

        
        text_score = (f"Skóre: {self.score:06d}")
        text_lives = (f"Životy: {self.lives}")
        text_wave = (f"Vlna: {self.curr_wave:02d}")
        text_pause = (f"P pro pauzu")

        self.outlined_text(text_score, self.basic_text, (255,255,255), (0,255, 0), (85,20))
        self.outlined_text(text_lives, self.basic_text, (255,255,255), (0,255,0), (50, 50))
        self.outlined_text(text_wave, self.basic_text, (255,255,255), (0,255, 0), (50 , 80))
        self.outlined_text(text_pause, self.basic_text, (255,255,255), (0,255, 0), (725, 20))
        


        # vykresleni mezipauzy u vln
        if self.wave_pause and not self.curr_wave == 0:
            inp =self.outlined_text((f"Vlna {self.curr_wave} dokoncena"), self.font_menu, (255,255,255), (255,255, 0), (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self._draw_game_status(inp, None, (0, 0, 255))
        # vykresleni pauzy
        if self.paused:
            txt1=self.shadow_text("HRA POZASTAVENA!", self.font_menu, (255, 255, 255), (255,255,0), (WINDOW_WIDTH // 2, (WINDOW_HEIGHT // 2) - 30))
            self._draw_game_status(txt1, "R pro restart / Q pro ukončení", (255, 0, 0))

        if self.state == "VICTORY" or self.state == "GAME_OVER":
            self._draw_endscreen(self.state)
        
        if self.state == "HIGHSCORE":
            self._draw_hs()

        # tohle je jakoby probliknuti
        if self.flash_timer > 0 and self.state == "PLAYING":
            flash_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            flash_surf.set_alpha(180) # semi-transparentni
            flash_surf.fill((255, 255, 255)) # bila
            self.screen.blit(flash_surf, (0, 0))

        pygame.display.flip()

    def _load_highscores(self):
        """
        funkce pro nacteni zebricku
        """
        if not os.path.exists("highscores.json"):
            return []
    
        with open("highscores.json", 'r') as f:
            return json.load(f)
    
    def _save_highscore(self):
        """
        funkce pro ukladani zebricku
        """
        entry = {
            "name" : self.player_name,
            "score" : self.score
        }
        self.highscores.append(entry)

        self.highscores.sort(key=lambda x: x["score"], reverse=True)

        self.highscores = self.highscores[:5]

        with open("highscores.json", 'w') as f:
            json.dump(self.highscores, f, indent=2)

    def _play_music(self, music: pygame.mixer.Sound, loop=True):
        """
        konecne muzeme hrat hudbicku ve smycce :3
        """
        if self.curr_music != music:
            pygame.mixer.stop()
            self.curr_music = music
            music.play(-1 if loop else 0)
        
    def _apply_volume(self):
        """
        funkce pro nastaveni hlasitosti
        """
        self.menu_song.set_volume(self.music_vol)
        self.play_song.set_volume(self.music_vol)

        self.shoot_sound.set_volume(self.sfx_vol * 0.6)
        self.boss_hit_player_sound.set_volume(self.sfx_vol * 0.6)
        self.collision_sound.set_volume(self.sfx_vol *  0.7)
        self.explosion_boss_sound.set_volume(self.sfx_vol * 0.6)
        self.losing_sound.set_volume(0.6 * self.sfx_vol)
        
    def shadow_text(self, text, font, color, shadow_color, center):
        """
        funkce pro text se stinem
        """
        shadow = font.render(text, True, shadow_color)
        text_surf = font.render(text, True, color)

        text_rect = text_surf.get_rect(center=center)
        shadow_rect = shadow.get_rect(center=(center[0] +2, center[1]+2))

        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(text_surf, text_rect)

    def outlined_text(self, text, font, color, outline, center):
        """
        funkce pro obtazeny text
        """
        base_text = font.render(text, True, color)
        outline_text = font.render(text, True, outline)

        base_rect = base_text.get_rect(center=center)

        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            outline_rect = outline_text.get_rect(center=(center[0]+dx, center[1]+dy))
            self.screen.blit(outline_text, outline_rect)
        
        self.screen.blit(base_text, base_rect)