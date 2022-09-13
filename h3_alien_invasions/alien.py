import pygame
from pygame.sprite import Sprite


class Aliens:
    def __init__(self, alien_group, settings, screen, ship, lasers):
        self.aliens = alien_group
        self.settings = settings
        self.screen = screen
        self.model_alien = Alien(self.settings, self.screen)
        self.ship = ship
        self.lasers = lasers

    def get_number_aliens_x(self, alien_width):
        """Determine the number of aliens that fit in a row."""
        available_space_x = self.settings.screen_width - 2 * alien_width
        number_aliens_x = int(available_space_x / (2 * alien_width))
        return number_aliens_x

    def get_number_rows(self, ship_height, alien_height):
        """Determine the number of rows of aliens that fit on the screen."""
        available_space_y = (
            self.settings.screen_height - (3 * alien_height) - ship_height
        )
        number_rows = int(available_space_y / (2 * alien_height))
        return number_rows

    def create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(settings=self.settings, screen=self.screen)
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def create_fleet(self):
        """Create a full fleet of aliens."""
        number_aliens_x = self.get_number_aliens_x(self.model_alien.rect.width)
        number_rows = self.get_number_rows(
            self.ship.rect.height, self.model_alien.rect.height
        )

        # Create the fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self.create_alien(alien_number, row_number)

    def check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction.x *= -1

    def update_lasers(self):
        pygame.sprite.groupcollide(self.lasers, self.aliens, True, True)
        if len(self.aliens) == 0:
            # Destroy existing bullets and create new fleet.
            self.lasers.empty()
            self.create_fleet()

    def update(self):
        self.check_fleet_edges()
        self.aliens.update()
        self.update_lasers()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship hit!!!")

    def draw(self):
        for alien in self.aliens.sprites():
            alien.draw()


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, settings, screen):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = screen
        self.settings = settings

        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def update(self):
        self.x += self.settings.alien_speed_factor * self.settings.fleet_direction.x
        self.rect.x = self.x

        self.draw()

    def draw(self):
        self.screen.blit(self.image, self.rect)
