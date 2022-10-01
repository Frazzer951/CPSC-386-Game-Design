from alien import Aliens
from barrier import Barriers
from button import Button
from laser import Lasers, LaserType
from pathlib import Path
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship
from sound import Sound
from time import time
import game_functions as gf
import pygame as pg
import sys


class Game:
    def __init__(self):
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height  # tuple
        self.screen = pg.display.set_mode(size=size)

        self.sound = Sound(bg_music="sounds/startrek.wav")
        self.scoreboard = Scoreboard(game=self)

        self.ship_lasers = Lasers(settings=self.settings, type=LaserType.SHIP)
        self.alien_lasers = Lasers(settings=self.settings, type=LaserType.ALIEN)

        self.barriers = Barriers(game=self)
        self.ship = Ship(game=self)
        self.aliens = Aliens(game=self)

        self.settings.initialize_speed_settings()

        self.gameover = False

    def reset(self):
        print("Resetting game...")
        self.barriers.reset()
        self.ship.reset()
        self.aliens.reset()
        # self.scoreboard.reset()

    def game_over(self):
        print("All ships gone: game over!")
        self.sound.gameover()
        self.gameover = True
        self.sound.stop_bg()

        file = Path("highscores.dat")
        file.touch(exist_ok=True)  # create the file if it doesn't exist
        scores = []
        with open("highscores.dat", "r") as file:
            file_content = file.read()
            scores = [] if len(file_content) == 0 else file_content.split(",")
            scores = [int(score) for score in scores]
            scores.append(self.scoreboard.score)
            scores.sort(reverse=True)
            scores = scores[:10]

        with open("highscores.dat", "w") as file:
            scores = str(scores).strip("[]")
            file.write(scores)

    def play(self):
        self.sound.play_bg()
        frametime = 1 / 60
        while True:  # at the moment, only exits in gf.check_events if Ctrl/Cmd-Q pressed
            if self.gameover:
                break

            start_time = time()
            gf.check_events(settings=self.settings, ship=self.ship)
            self.screen.fill(self.settings.bg_color)
            self.ship.update()
            self.aliens.update()
            self.barriers.update()
            self.scoreboard.update()
            pg.display.flip()
            elapsed = time() - start_time
            while elapsed < frametime:  # run with a max fps of 60
                elapsed = time() - start_time


class Menu:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height  # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Alien Invasion")

        self.alien0 = pg.image.load("images/alien0_0.png")
        self.alien1 = pg.image.load("images/alien1_0.png")
        self.alien2 = pg.image.load("images/alien2_0.png")
        self.ufo = pg.image.load("images/ufo_0.png")
        self.play_button = Button((self.screen.get_rect().centerx, 600), "PLAY", Menu.get_font(45), "#DDDDDD", "#00FF00")
        self.high_scores_button = Button(
            (self.screen.get_rect().centerx, 650), "HIGH SCORES", Menu.get_font(45), "#DDDDDD", "#00FF00"
        )

    def get_font(size):
        return pg.font.SysFont(None, size)

    def draw_logo(self):
        space_text = Menu.get_font(130).render("SPACE", True, "#FFFFFF")
        space_rect = space_text.get_rect()
        space_rect.left = self.screen.get_rect().centerx - space_rect.width / 2
        space_rect.top = 20
        self.screen.blit(space_text, space_rect)

        invaders_text = Menu.get_font(80).render("INVADERS", True, "#00FF00")
        invaders_rect = invaders_text.get_rect()
        invaders_rect.left = self.screen.get_rect().centerx - invaders_rect.width / 2
        invaders_rect.top = 100
        self.screen.blit(invaders_text, invaders_rect)

    def draw_alien_points(self, image, text, position):
        image_rect = image.get_rect()
        image_rect.left = position[0]
        image_rect.top = position[1]
        self.screen.blit(image, image_rect)

        text = Menu.get_font(45).render(text, True, "#DDDDDD")
        text_rect = text.get_rect()
        text_rect.left = position[0] + image_rect.width + 40
        text_rect.top = position[1] + image_rect.height / 4
        self.screen.blit(text, text_rect)

    def start_screen(self):
        while True:
            self.screen.fill((0, 0, 0))

            mouse_pos = pg.mouse.get_pos()

            self.draw_logo()
            self.draw_alien_points(image=self.alien0, text="= 10 PTS", position=(460, 200))
            self.draw_alien_points(image=self.alien1, text="= 10 PTS", position=(460, 280))
            self.draw_alien_points(image=self.alien2, text="= 10 PTS", position=(460, 360))
            self.draw_alien_points(image=self.ufo, text="= 10 PTS", position=(410, 440))
            self.play_button.setHover(mouse_pos)
            self.high_scores_button.setHover(mouse_pos)

            self.play_button.draw(self.screen)
            self.high_scores_button.draw(self.screen)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.play_button.onButton(mouse_pos):
                        self.play()
                    elif self.high_scores_button.onButton(mouse_pos):
                        self.highscores()

            pg.display.flip()

    def highscores(self):
        pass

    def play(self):
        g = Game()
        g.play()


def main():
    m = Menu()
    m.start_screen()


if __name__ == "__main__":
    main()
