import pygame
from game_functions import clamp
from pygame.sprite import Sprite
from vector import Vector


class Ship(Sprite):
    def __init__(self, settings, screen, sound, lasers=None):
        super().__init__()
        self.settings = settings
        self.screen = screen
        self.sound = sound

        self.image = pygame.image.load("images/ship.bmp")

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # posn is the centerx, bottom of the rect, not left, top
        self.posn = self.center_ship()

        self.vel = Vector()
        self.lasers = lasers
        self.shooting = False
        self.lasers_attempted = 0

    def center_ship(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        return Vector(self.rect.left, self.rect.top)

    def update(self):
        self.posn += self.vel
        self.posn, self.rect = clamp(self.posn, self.rect, self.settings)
        if self.shooting:
            self.lasers_attempted += 1
            if self.lasers_attempted % self.settings.lasers_every == 0:
                self.lasers.shoot(
                    settings=self.settings,
                    screen=self.screen,
                    ship=self,
                    sound=self.sound,
                )
        self.draw()

    def draw(self):
        self.screen.blit(self.image, self.rect)
