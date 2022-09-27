from random import randrange
import pygame as pg
from pygame.sprite import Sprite, Group
from timer import Timer


class Alien(Sprite):
    alien_images0 = [pg.image.load(f"images/alien0_{n}.png") for n in range(2)]
    alien_images1 = [pg.image.load(f"images/alien1_{n}.png") for n in range(2)]
    alien_images2 = [pg.image.load(f"images/alien2_{n}.png") for n in range(2)]
    # alien_images3 = [pg.image.load(f"images/alien3_{n}.png") for n in range(2)]

    alien_timers = {
        0: Timer(image_list=alien_images0),
        1: Timer(image_list=alien_images1),
        2: Timer(image_list=alien_images2),
        # 3: Timer(image_list=alien_images3),
    }

    alien_explosion_images = [pg.image.load(f"images/explode{n}.png") for n in range(7)]

    def __init__(self, game, type):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.sound = game.sound
        self.image = pg.image.load("images/alien0.bmp")
        self.rect = self.image.get_rect()
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.type = type

        self.alien_lasers = game.alien_lasers
        self.shoot_delay = randrange(10_000, 100_000)
        self.last_shoot_time = pg.time.get_ticks()

        self.dying = self.dead = False

        # self.timer_normal = Timer(image_list=self.alien_images)
        # self.timer_normal = Timer(image_list=self.alien_types[type])

        self.timer_normal = Alien.alien_timers[type]
        self.timer_explosion = Timer(image_list=Alien.alien_explosion_images, is_loop=False)
        self.timer = self.timer_normal

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def check_bottom_or_ship(self, ship):
        screen_rect = self.screen.get_rect()
        return self.rect.bottom >= screen_rect.bottom or self.rect.colliderect(ship.rect)

    def hit(self):
        if not self.dying:
            self.dying = True
            self.timer = self.timer_explosion

    def update(self):
        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.kill()
        settings = self.settings
        self.x += settings.alien_speed_factor * settings.fleet_direction
        self.rect.x = self.x

        if pg.time.get_ticks() - self.shoot_delay >= self.last_shoot_time:
            self.last_shoot_time = pg.time.get_ticks()
            self.alien_lasers.shoot(ship=self)

        self.draw()

    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)
        # self.screen.blit(self.image, self.rect)


class Aliens:
    def __init__(self, game):
        self.model_alien = Alien(game=game, type=1)
        self.game = game
        self.sb = game.scoreboard
        self.aliens = Group()
        self.lasers = game.lasers.lasers  # a laser Group
        self.alien_lasers = game.alien_lasers
        self.screen = game.screen
        self.settings = game.settings
        self.sound = game.sound
        self.ship = game.ship
        self.create_fleet()

    def reset(self):
        self.aliens.empty()
        self.create_fleet()

    def create_alien(self, alien_number, row_number):
        if row_number > 5:
            raise ValueError("row number must be less than 6")
        type = (row_number // 2) % 3
        alien = Alien(game=self.game, type=type)
        alien_width = alien.rect.width

        alien.x = alien_width + 1.2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = 2 * alien.rect.height + 1.2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def create_fleet(self):
        number_aliens_x = 11
        number_rows = 5
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self.create_alien(alien_number, row_number)

    def check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def check_fleet_bottom(self):
        for alien in self.aliens.sprites():
            if alien.check_bottom_or_ship(self.ship):
                self.ship.die()
                break

    def check_fleet_empty(self):
        if len(self.aliens.sprites()) == 0:
            print("Aliens all gone!")
            self.game.reset()

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def check_collisions(self):
        collisions = pg.sprite.groupcollide(self.aliens, self.lasers, False, True)
        if collisions:
            for alien in collisions:
                alien.hit()
            self.sb.increment_score()

    def update(self):
        self.check_fleet_edges()
        self.check_fleet_bottom()
        self.check_collisions()
        self.check_fleet_empty()
        for alien in self.aliens.sprites():
            if alien.dead:  # set True once the explosion animation has completed
                alien.remove()
            alien.update()

    def draw(self):
        for alien in self.aliens.sprites():
            alien.draw()
