import pygame


class bullet():
    def __init__(self,):
        bulletImg = pygame.image.load('bullets.png')
        bulletX = 0
        bulletY = 500
        bulletX_change = 5
        bulletY_change = 0.3
        bullet_state = "ready"