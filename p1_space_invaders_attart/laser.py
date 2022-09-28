import pygame as pg
from pygame.sprite import Sprite, Group
from timer import Timer
from random import randint


class Lasers:
    def __init__(self, game, shoot_down=False):
        self.lasers = Group()
        self.settings = game.settings
        self.screen = game.screen
        self.shoot_down = shoot_down

    def reset(self):
        self.lasers.empty()

    def shoot(self, ship):
        self.lasers.add(Laser(game=self.game, ship=ship, shoot_down=self.shoot_down))

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

    laser_images = [pg.transform.rotozoom(pg.image.load(f"images/laser_{n}.png"), 0, 1) for n in range(4)]
    alien_laser_images = [pg.transform.rotozoom(pg.image.load(f"images/alien_laser{n}.png"), 0, 1) for n in range(7)]

    laser_timers = {
        False: Timer(image_list=laser_images),
        True: Timer(image_list=alien_laser_images),
    }

    def __init__(self, game, ship, shoot_down=False):
        super().__init__()
        self.screen = game.screen
        self.rect = pg.Rect(0, 0, game.settings.laser_width, game.settings.laser_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.bottom = ship.rect.top
        self.y = float(self.rect.y)
        self.color = (randint(0, 200), randint(0, 200), randint(0, 200))
        self.speed_factor = game.settings.laser_speed_factor
        if shoot_down:
            self.speed_factor *= -1
        self.timer = Laser.laser_timers[shoot_down]
        game.sound.shoot_laser()

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y
        self.draw()

    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)
        # pg.draw.rect(self.screen, self.color, self.rect)
