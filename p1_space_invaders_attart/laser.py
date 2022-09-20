import pygame as pg
from pygame.sprite import Sprite, Group
from random import randint


class Lasers:
    def __init__(self, settings, screen, shoot_down=False):
        self.lasers = Group()
        self.settings = settings
        self.screen = screen
        self.shoot_down = shoot_down

    def reset(self):
        self.lasers.empty()

    def shoot(self, settings, screen, ship, sound):
        self.lasers.add(Laser(settings=settings, screen=screen, ship=ship, sound=sound, shoot_down=self.shoot_down))

    def update(self):
        self.lasers.update()
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0 or laser.rect.top >= self.screen.get_rect().bottom:
                self.lasers.remove(laser)

    def draw(self):
        for laser in self.lasers.sprites():
            laser.draw()


class Laser(Sprite):
    """A class to manage lasers fired from the ship"""

    def __init__(self, settings, screen, ship, sound, shoot_down=False):
        super().__init__()
        self.screen = screen
        self.rect = pg.Rect(0, 0, settings.laser_width, settings.laser_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.bottom = ship.rect.top
        self.y = float(self.rect.y)
        self.color = (randint(0, 200), randint(0, 200), randint(0, 200))
        self.speed_factor = settings.laser_speed_factor
        if shoot_down:
            self.speed_factor *= -1
        sound.shoot_laser()

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y
        self.draw()

    def draw(self):
        pg.draw.rect(self.screen, self.color, self.rect)
