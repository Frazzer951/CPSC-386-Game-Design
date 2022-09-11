import pygame
from pygame.sprite import Sprite
from game_functions import clamp
from vector import Vector


class Ship(Sprite):
    def __init__(self, settings, screen, sound, lasers=None):
        super().__init__()
        # TODO: save screen, settings, and sound in self
        # TODO: load the image of images/ship.bmp
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.posn = (
            self.center_ship()
        )  # posn is the centerx, bottom of the rect, not left, top
        self.center_ship()

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
        clamp(self.rect, self.settings)
        if self.shooting:
            print("shooting lasers")
            self.lasers_attempted += 1
            if self.lasers_attempted % self.settings.lasers_every == 0:
                self.lasers.shoot(
                    settings=self.settings,
                    screen=self.screen,
                    ship=self,
                    sound=self.sound,
                )
        self.rect.centerx = self.posn.x + self.rect.width / 2
        self.rect.centery = self.posn.y + self.rect.height / 2
        self.draw()

    def draw(self):
        pass  # TODO: remove this line
        # TODO: implement draw for ship
