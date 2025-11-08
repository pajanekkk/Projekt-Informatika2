import pygame
from pygame.locals import *
from settings import *
import sys


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



   
    clock.tick(FPS)
    fps = clock.get_fps()
    pygame.display.set_caption(f"FPS: {fps:.0f}")
    pygame.display.flip()

pygame.quit()