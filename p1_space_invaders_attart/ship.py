from game_functions import clamp
from pygame.sprite import Sprite
from timer import Timer
from vector import Vector
import pygame as pg


class Ship(Sprite):
    ship_images = [pg.image.load(f"images/ship_{n}.png") for n in range(2)]

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.sound = game.sound
        self.ships_left = game.settings.ship_limit
        self.image = pg.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = game.screen.get_rect()
        self.posn = self.center_ship()  # posn is the centerx, bottom of the rect, not left, top
        self.vel = Vector()
        self.lasers = game.ship_lasers
        self.shooting = False
        self.lasers_attempted = 0
        self.timer = Timer(image_list=Ship.ship_images, delay=200)

    def center_ship(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 10
        return Vector(self.rect.left, self.rect.top)

    def reset(self):
        self.vel = Vector()
        self.posn = self.center_ship()
        self.lasers.reset()
        self.rect.left, self.rect.top = self.posn.x, self.posn.y

    def die(self):
        self.ships_left -= 1
        print(f"Ship is dead! Only {self.ships_left} ships left")
        self.game.reset() if self.ships_left > 0 else self.game.game_over()

    def update(self):
        self.posn += self.vel
        self.posn, self.rect = clamp(self.posn, self.rect, self.settings)
        if self.shooting:
            self.lasers_attempted += 1
            if self.lasers_attempted % self.settings.lasers_every == 0:
                self.lasers.shoot(game=self.game, x=self.rect.centerx, y=self.rect.top)
        self.lasers.update()
        self.draw()

    def draw(self):
        image = self.timer.image()
        self.screen.blit(image, self.rect)
