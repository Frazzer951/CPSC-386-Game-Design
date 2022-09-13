import pygame as pg
from settings import Settings
import game_functions as gf
from pygame.sprite import Group

from laser import Lasers
from ship import Ship
from sound import Sound


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height  # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Alien Invasion")

        self.sound = Sound(bg_music="sounds/startrek.wav")

        laser_group = Group()
        self.lasers = Lasers(laser_group=laser_group, settings=self.settings)
        self.ship = Ship(
            settings=self.settings,
            screen=self.screen,
            sound=self.sound,
            lasers=self.lasers,
        )

        self.settings.initialize_speed_settings()

    def play(self):
        self.sound.play_bg()
        while True:
            gf.check_events(settings=self.settings, ship=self.ship)

            self.screen.fill(self.settings.bg_color)

            self.lasers.update()
            self.ship.update()

            pg.display.flip()


def main():
    g = Game()
    g.play()


if __name__ == "__main__":
    main()
