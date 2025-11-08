import pygame
from pygame.locals import *
from settings import *
import sys

import random

class Hrac:
    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y

        self.rychl_x = x
        self.rychl_y = y


        self.width = 50
        self.height = 60
        self.on_ground = False

    def klavesy_pohyb(self):
        zmack_klavesa = pygame.key.get_pressed()
        if zmack_klavesa[pygame.K_RIGHT]:
            self.rychl_x = +RYCHLOST_POHYBU
        elif zmack_klavesa[pygame.K_LEFT]:
            self.rychl_x = -RYCHLOST_POHYBU
        else:
            self.rychl_x = 0

        if zmack_klavesa[pygame.K_SPACE] and self.on_ground == True:
            self.rychl_y = RYCHLOST_SKOKU
            self.on_ground = False
    
    def gravitace(self):
        if self.on_ground == False:
            self.rychl_y += GRAVITACE
    
    def aktualizuj(self):
        self.pos_x += self.rychl_x
        self.pos_y += self.rychl_y

        spodek = HEIGHT - 100
        if self.pos_y + self.height >= spodek:
            self.pos_y = spodek - self.height
            self.vel_y = 0
            self.on_ground = True
    
    def vykresli(self, surface):
        pygame.draw.rect(surface, (100,200,100), (self.pos_x, self.pos_y, self.width, self.height))
            