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
        # TODO: make a Sound object using the music sounds/startrek.wav (or any other appropriate music)
        laser_group = Group()  # TODO: look up what a Group() is on pygame.org
        # TODO: create the lasers and the ship
        # TODO: initialize the speed settings

    def play(self):
        # TODO: play the background music
        while (
            True
        ):  # at the moment, only exits in gf.check_events if Ctrl/Cmd-Q pressed
            # TODO: check for events
            self.screen.fill(self.settings.bg_color)
            # TODO: make the ship and lasers update and draw, each with a single function call
            pg.display.flip()


def main():
    g = Game()
    g.play()


if __name__ == "__main__":
    main()
