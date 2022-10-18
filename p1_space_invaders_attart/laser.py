from enum import Enum
from random import randint

import pygame as pg
from pygame.sprite import Group, Sprite
from timer import Timer


class LaserType(Enum):
    ALIEN = 1
    SHIP = 2


class Lasers:
    def __init__(self, settings, type):
        self.lasers = Group()
        self.settings = settings
        self.type = type

    def reset(self):
        self.lasers.empty()

    def shoot(self, game, x, y):
        self.lasers.add(Laser(settings=game.settings, screen=game.screen, x=x, y=y, sound=game.sound, type=self.type))

    def update(self):
        self.lasers.update()
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0 or laser.rect.top >= 800:
                self.lasers.remove(laser)

    def draw(self):
        for laser in self.lasers.sprites():
            laser.draw()


class Laser(Sprite):
    """A class to manage lasers fired from the ship"""

    alien_laser_images = [pg.image.load(f"images/laser_alien_{n}.png") for n in range(3)]
    ship_laser_images = [pg.image.load(f"images/laser_ship_{n}.png") for n in range(6)]
    laser_images = {LaserType.ALIEN: alien_laser_images, LaserType.SHIP: ship_laser_images}

    laser_explosion_images = [pg.image.load(f"images/explosion_{n}.png") for n in range(7)]

    def __init__(self, settings, screen, x, y, sound, type):
        super().__init__()
        self.screen = screen
        self.rect = pg.Rect(0, 0, settings.laser_width, settings.laser_height)
        self.rect.centerx = x
        self.rect.bottom = y
        self.y = float(self.rect.y)
        self.type = type
        self.color = (randint(0, 200), randint(0, 200), randint(0, 200))
        self.speed_factor = settings.laser_speed_factor
        imagelist = Laser.laser_images[type]
        self.timer = Timer(image_list=imagelist)
        self.timer_explosion = Timer(image_list=Laser.laser_explosion_images, is_loop=False)
        self.dying = False
        sound.shoot_laser()

    def hit(self):
        if not self.dying:
            self.dying = True
            self.timer = self.timer_explosion

    def update(self):
        self.y += self.speed_factor if self.type == LaserType.ALIEN else -self.speed_factor
        self.rect.y = self.y
        self.draw()

    def draw(self):
        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.kill()
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)
