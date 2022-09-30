import pygame as pg
from pygame.sprite import Sprite, Group


class Barriers:
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.barriers = Group()

        self.create_barriers()

    def create_barriers(self):
        rect = Barrier.barriers[0].get_rect()
        width = rect.width
        height = rect.height
        top = self.settings.screen_height - 2.1 * height
        for i in range(5):
            barrier = Barrier(game=self.game, x=i * 1.5 * width + width, y=top)
            self.barriers.add(barrier)

    def reset(self):
        self.barriers.empty()
        self.create_barriers()

    def update(self):
        for barrier in self.barriers:
            barrier.update()


class Barrier(Sprite):
    color = 255, 0, 0

    barriers = [pg.image.load(f"images/barrier_{n}.png") for n in range(6)]

    def __init__(self, game, x, y):
        super().__init__()
        self.settings = game.settings
        self.screen = game.screen
        self.damage = 0
        self.image = Barrier.barriers[0]
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y

    def hit(self):
        self.damage += 1
        if self.damage >= 6:
            self.kill()
        else:
            self.image = Barrier.barriers[self.damage]

    def update(self):
        self.draw()

    def draw(self):
        # rect = self.image.get_rect()
        # rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(self.image, self.rect)
        # pg.draw.rect(self.screen, Barrier.color, self.rect, 0, 20)
        # pg.draw.circle(self.screen, self.settings.bg_color, (self.rect.centerx, self.rect.bottom), self.rect.width / 6)
