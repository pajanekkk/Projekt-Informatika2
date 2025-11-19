import pygame
from src.player import *
from src.settings import *
import random
import sys

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Space defender")

        self.clock = pygame.time.Clock()

        self.running = True

    def run(self):
        while self.running:
            self._draw()
    
    def _draw(self):
        self.screen.fill((0, 255, 255))
        pygame.display.flip()