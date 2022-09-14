from asyncio import ReadTransport
import pygame as pg
from pygame.sprite import Sprite, Group
from laser import Lasers


class Aliens:
    def __init__(self, game, screen, settings, lasers: Lasers, ship):
        self.model_alien = Alien(settings=settings, screen=screen)
        self.game = game
        self.aliens = Group()
        self.lasers = lasers.lasers  # a laser Group
        self.screen = screen
        self.settings = settings
        self.ship = ship
        self.create_fleet()

    def get_number_aliens_x(self, alien_width):
        available_space_x = self.settings.screen_width - 2 * alien_width
        # TODO: use book's code to correct the calculation for number_aliens_x
        number_aliens_x = None
        return number_aliens_x

    def get_number_rows(self, ship_height, alien_height):
        available_space_y = (
            self.settings.screen_height - (3 * alien_height) - ship_height
        )
        # TODO: use book's code to correct the calculation for number_rows
        number_rows = None
        return number_rows

    def reset(self):
        pass  # TODO: write the code to reset the fleet

    def create_alien(self, alien_number, row_number):
        alien = Alien(settings=self.settings, screen=self.screen)
        alien_width = alien.rect.width

        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        # TODO: add an alien to aliens

    def create_fleet(self):
        number_aliens_x = self.get_number_aliens_x(self.model_alien.rect.width)
        number_rows = self.get_number_rows(
            self.ship.rect.height, self.model_alien.rect.height
        )
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                pass  # TODO: remove this line
                # TODO: create an alien with alien_number and row_number
                #       see book's code for help

    def check_fleet_edges(self):
        for alien in self.aliens.sprites():
            pass  # TODO: remove this line after the code below is written
            #        for each Alien to check edges and change fleet direction
            #        if necessary

    def check_fleet_bottom(self):
        pass  # TODO: remove this line
        # TODO: fill in the code to check if the fleet has hit the bottom or hit the ship
        #       in either case, it should call self.ship.die() and break

    def check_fleet_empty(self):
        if len(self.aliens.sprites()) == 0:
            print("Aliens all gone!")
        # TODO: reset the game if the fleet is empty

    def change_fleet_direction(self):
        pass  # TODO: fill in the code to change the fleet direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def check_collisions(self):
        collisions = pg.sprite.groupcollide(
            self.lasers, self.aliens, True, True
        )  # first True means eliminate laser, ...

    def update(self):
        self.check_fleet_edges()
        self.check_fleet_bottom()
        self.check_collisions()
        self.check_fleet_empty()
        for alien in self.aliens.sprites():
            alien.update()

    def draw(self):
        for alien in self.aliens.sprites():
            alien.draw()


class Alien(Sprite):
    def __init__(self, settings, screen):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.image = pg.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return False  # TODO: remove this line and replace it to see if the Alien
        #       has hit the right or left edge of the screen_ect

    def check_bottom_or_ship(self, ship):
        screen_rect = self.screen.get_rect()
        return False  # TODO: remove this line and replace it with the code
        #       to see if the Alien has hit the ship or the bottom
        #       of the screen

    def update(self):
        settings = self.settings
        self.x += settings.alien_speed_factor * settings.fleet_direction
        self.rect.x = self.x
        self.draw()

    def draw(self):
        self.screen.blit(self.image, self.rect)
