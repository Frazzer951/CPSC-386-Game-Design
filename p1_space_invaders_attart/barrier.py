import pygame as pg
from pygame.sprite import Sprite


class Barriers:
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.create_barriers()

    def create_barriers(self):
        width = self.settings.screen_width / 10
        height = 2.0 * width / 4.0
        top = self.settings.screen_height - 2.1 * height
        self.barriers = [
            Barrier(game=self.game, rect=pg.Rect(x * 2 * width + 1.5 * width, top, width, height)) for x in range(4)
        ]

    def reset(self):
        self.create_barriers()

    def update(self):
        for barrier in self.barriers:
            barrier.update()


class Barrier(Sprite):
    color = (255, 0, 0)

    def __init__(self, game, rect):
        super().__init__()
        self.settings = game.settings
        self.screen = game.screen
        self.rect = rect

    def hit(self):
        pass

    def update(self):
        self.draw()

    def draw(self):
        pg.draw.rect(self.screen, Barrier.color, self.rect, 0, 15)
        pg.draw.circle(self.screen, self.settings.bg_color, (self.rect.centerx, self.rect.bottom), self.rect.width / 4)
