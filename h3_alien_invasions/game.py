from time import sleep
import pygame as pg
from settings import Settings
import game_functions as gf

from alien import Aliens
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

        print("THIS CODE WILL NOT RUN UNTIL YOU FIX ALL OF THE TODO STATEMENTS")
        print("    Well, actually, as you implement the TODOs, more and more of the code will run")
        print("    Be sure that ALL of the features in chapter 13 are working by the time you are done")
        print("    Submit the zip file of the project folder, AND")
        print("    a GIF file showing the features of the program: Aliens, lasers destroying them,")
        print("    Aliens bouncing off the walls, killing the ship if they hit it or hit the bottom")
        print("    You do NOT have to implement a Game_Stat class")

        self.lasers = Lasers(settings=self.settings)
        self.ship = Ship(
            game=self,
            screen=self.screen,
            settings=self.settings,
            sound=self.sound,
            lasers=self.lasers,
        )
        self.aliens = Aliens(
            game=self,
            screen=self.screen,
            settings=self.settings,
            lasers=self.lasers,
            ship=self.ship,
        )
        self.settings.initialize_speed_settings()

    def reset(self):
        print("Resetting game...")
        self.lasers.reset()
        self.aliens.reset()
        self.ship.reset()

    def game_over(self):
        print("All ships gone: game over!")
        self.sound.gameover()
        exit()

    def play(self):
        self.sound.play_bg()
        while True:  # at the moment, only exits in gf.check_events if Ctrl/Cmd-Q pressed
            gf.check_events(settings=self.settings, ship=self.ship)
            self.screen.fill(self.settings.bg_color)
            self.ship.update()
            self.aliens.update()
            self.lasers.update()
            pg.display.flip()
            sleep(0.01)  # Slow game down so it is playable


def main():
    g = Game()
    g.play()


if __name__ == "__main__":
    main()
