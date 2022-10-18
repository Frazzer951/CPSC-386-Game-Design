from random import randint

import pygame as pg
from pygame.sprite import Group, Sprite
from timer import Timer


class Alien(Sprite):
    alien_images0 = [pg.image.load(f"images/alien0_{n}.png") for n in range(2)]
    alien_images1 = [pg.image.load(f"images/alien1_{n}.png") for n in range(2)]
    alien_images2 = [pg.image.load(f"images/alien2_{n}.png") for n in range(2)]

    alien_timers = {
        0: Timer(image_list=alien_images0, delay=200),
        1: Timer(image_list=alien_images1, delay=200),
        2: Timer(image_list=alien_images2, delay=200),
    }

    alien_explosions0 = [pg.image.load(f"images/explosion_10_{n}.png") for n in range(7)]
    alien_explosions1 = [pg.image.load(f"images/explosion_20_{n}.png") for n in range(7)]
    alien_explosions2 = [pg.image.load(f"images/explosion_40_{n}.png") for n in range(7)]

    alien_explosions = {
        0: alien_explosions0,
        1: alien_explosions1,
        2: alien_explosions2,
    }

    alien_points = {
        0: 10,
        1: 20,
        2: 40,
    }

    def __init__(self, game, type):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.sb = game.scoreboard
        self.image = pg.image.load("images/alien0_0.png")
        self.rect = self.image.get_rect()
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.type = type
        self.points = Alien.alien_points[type]
        self.dying = self.dead = False

        # self.timer_normal = Timer(image_list=self.alien_images)
        # self.timer_normal = Timer(image_list=self.alien_types[type])

        self.timer_normal = Alien.alien_timers[type]
        self.timer_explosion = Timer(image_list=Alien.alien_explosions[type], delay=200, is_loop=False)
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
            self.sb.increment_score(self.points)

    def update(self):
        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.kill()
        settings = self.settings
        self.x += settings.alien_speed_factor * settings.fleet_direction
        self.rect.x = self.x
        self.draw()

    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)
        # self.screen.blit(self.image, self.rect)


class UFO(Alien):
    ufo_image = [pg.image.load(f"images/ufo_{n}.png") for n in range(2)]

    def __init__(self, game):
        super().__init__(game=game, type=0)
        self.image = pg.image.load("images/ufo_0.png")
        self.rect = self.image.get_rect()
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.points = randint(1, 1000)
        self.text_color = (30, 30, 30)
        self.font = pg.font.SysFont(None, 48)
        self.dying = self.dead = False
        self.timer = Timer(image_list=UFO.ufo_image, delay=200)
        self.points_image = None
        self.points_rect = None
        self.death_counter = 0

        print(f"UFO Worth {self.points} points")

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def hit(self):
        if not self.dying:
            self.dying = True
            self.sb.increment_score(self.points)

            points_str = str(self.points)
            self.points_image = self.font.render(points_str, True, self.text_color, self.settings.bg_color)
            self.points_rect = self.points_image.get_rect()
            self.points_rect.left = self.rect.left
            self.points_rect.top = self.rect.top

    def isDead(self):
        return self.dead or self.check_edges()

    def update(self):
        if self.dying is True:
            self.death_counter += 1
            if self.death_counter >= 300:
                self.dead = True
        else:
            self.x += self.settings.alien_speed_factor
            self.rect.x = self.x
        self.draw()

    def draw(self):
        if self.dying is True:
            self.screen.blit(self.points_image, self.points_rect)
        else:
            image = self.timer.image()
            rect = image.get_rect()
            rect.left, rect.top = self.rect.left, self.rect.top
            self.screen.blit(image, rect)


class Aliens:
    def __init__(self, game):
        self.model_alien = Alien(game=game, type=1)
        self.game = game
        self.sb = game.scoreboard
        self.aliens = Group()

        self.ship_lasers = game.ship_lasers.lasers  # a laser Group
        self.alien_lasers = game.alien_lasers

        self.screen = game.screen
        self.settings = game.settings
        self.shoot_requests = 0

        self.ufo_spawned = False
        self.spawn_request = 0
        self.ufo = None

        self.ship = game.ship
        self.create_fleet()

    def get_number_aliens_x(self, alien_width):
        available_space_x = self.settings.screen_width - 6 * alien_width
        number_aliens_x = int(available_space_x / (1.2 * alien_width))
        return number_aliens_x

    def reset(self):
        self.aliens.empty()
        self.create_fleet()
        self.alien_lasers.reset()
        self.ufo = None
        self.ufo_spawned = False

    def create_alien(self, alien_number, row_number):
        type = row_number // 2
        alien = Alien(game=self.game, type=type)
        alien_width = alien.rect.width

        alien.x = alien_width + 1.5 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = 1.5 * alien.rect.height + 1.2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def create_fleet(self):
        number_aliens_x = self.get_number_aliens_x(self.model_alien.rect.width)
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

    def shoot_from_random_alien(self):
        self.shoot_requests += 1
        if self.shoot_requests % self.settings.aliens_shoot_every != 0:
            return

        num_aliens = len(self.aliens.sprites())
        alien_num = randint(0, num_aliens)
        i = 0
        for alien in self.aliens.sprites():
            if i == alien_num:
                self.alien_lasers.shoot(game=self.game, x=alien.rect.centerx, y=alien.rect.bottom)
            i += 1

    def spawn_ufo(self):
        if self.ufo_spawned is False:
            self.spawn_request += 1
            if self.spawn_request % self.settings.ufo_spawn_rate != 0:
                return

            print("Spawning UFO")
            self.ufo_spawned = True

            ufo = UFO(game=self.game)
            ufo.x = 0
            ufo.rect.x = ufo.x
            ufo.rect.y = 0.2 * ufo.rect.height
            self.ufo = ufo

    def check_collisions(self):
        # ship_lasers hitting an alien
        collisions = pg.sprite.groupcollide(self.aliens, self.ship_lasers, False, True)
        if collisions:
            for alien in collisions:
                alien.hit()

        # ship_lasers hitting a barrier
        collisions = pg.sprite.groupcollide(self.game.barriers.barriers, self.ship_lasers, False, True)
        if collisions:
            for barrier in collisions:
                barrier.hit()

        # ship_lasers hitting the ufo
        if self.ufo_spawned:
            for laser in self.ship_lasers:
                if laser.rect.colliderect(self.ufo.rect):
                    self.ufo.hit()

        # alien_lasers hitting a barrier
        collisions = pg.sprite.groupcollide(self.game.barriers.barriers, self.alien_lasers.lasers, False, True)
        if collisions:
            for barrier in collisions:
                barrier.hit()

        # alien_lasers hitting the ship
        for laser in self.alien_lasers.lasers:
            if laser.rect.colliderect(self.ship.rect):
                self.ship.die()

        # alien_lasers hitting a ship_lasers
        collisions = pg.sprite.groupcollide(self.alien_lasers.lasers, self.ship_lasers, False, True)
        if collisions:
            for laser in collisions:
                laser.hit()

    def update(self):
        self.check_fleet_edges()
        self.check_fleet_bottom()
        self.check_collisions()
        self.check_fleet_empty()
        self.shoot_from_random_alien()
        self.spawn_ufo()

        for alien in self.aliens.sprites():
            if alien.dead:  # set True once the explosion animation has completed
                alien.remove()
            alien.update()

        if self.ufo_spawned:
            self.ufo.update()

            if self.ufo.isDead():
                self.ufo = None
                self.ufo_spawned = False

        self.alien_lasers.update()

    def draw(self):
        for alien in self.aliens.sprites():
            alien.draw()
