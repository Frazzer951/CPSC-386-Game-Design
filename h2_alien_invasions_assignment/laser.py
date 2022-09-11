import pygame as pg
from pygame.sprite import Sprite
from random import randint


class Lasers:
    def __init__(self, laser_group, settings):
        self.lasers = laser_group
        self.settings = settings

    def shoot(self, settings, screen, ship, sound):
        pass   # TODO: remove this line
        # TODO: fill in the code to add a laser to self.lasers

    def update(self):
        self.lasers.update()
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0:
                self.lasers.remove(laser)

    def draw(self):
        for laser in self.lasers.sprites():
            laser.draw()


class Laser(Sprite):
    """A class to manage lasers fired from the ship"""
    def __init__(self, settings, screen, ship, sound):
        super().__init__()
        self.screen = screen
        self.rect = pg.Rect(0, 0, settings.laser_width, settings.laser_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.bottom = ship.rect.top
        self.y = float(self.rect.y)
        # self.color = settings.laser_color
        self.color = (randint(0, 200), randint(0, 200), randint(0, 200))
        self.speed_factor = settings.laser_speed_factor
        sound.shoot_laser()

    def update(self):
        pass   # TODO: remove this line
        # TODO: update the lasers and draw them

    def draw(self):
        pass   # TODO: remove this line
        # TODO: draw the lasers  (use simple rectangles for now -- later we will use animated images)
