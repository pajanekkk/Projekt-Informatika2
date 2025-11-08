import pygame
from pygame.locals import *
from settings import *
from src.player import *
import sys
import random


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
bg = pygame.image.load('assets/wallpaper.png')
running = True
hrac = Hrac(50,50)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
   

    hrac.klavesy_pohyb()
    hrac.gravitace()
    hrac.aktualizuj()
  

    

    screen.blit(bg,(0,0))
    hrac.vykresli(screen)
    pygame.display.flip()


    clock.tick(FPS)
    fps = clock.get_fps()
    pygame.display.set_caption(f"FPS: {fps:.0f}")

pygame.quit()