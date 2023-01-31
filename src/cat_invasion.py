import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from mouse import Mouse
from bullet import Bullet
from cat import Cat


class CatInvasion:
    """A class for managing resources and game behavior."""

    def __init__(self):
        """Initializes the game and creates game resources."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height))

        self.background = pygame.image.load("..//recources/images/BG.png").convert()
        pygame.display.set_caption("Cat Invasion")

        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        self.mouse = Mouse(self)
        self.bullets = pygame.sprite.Group()
        self.cats = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, "Play")

    def _mouse_hit(self):
        """Handles a mouse collision with a cat."""

        if self.stats.mice_left > 0:

            self.stats.mice_left -= 1
            self.scoreboard.prep_mice()

            self.cats.empty()
            self.bullets.empty()

            self._create_fleet()
            self.mouse.center_mouse()

            sleep(2)

        else:

            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_cat(self, cat_number, row_number):
        # Create a cat and place it in a row
        cat = Cat(self)
        cat_width, cat_height = cat.rect.size
        cat.x = cat_width + cat_width * cat_number
        cat.rect.x = cat.x
        cat.rect.y = cat.rect.height + cat.rect.height * row_number

        self.cats.add(cat)

    def _create_fleet(self):
        """Creating an invasion fleet"""
        # Create a cat and calculate the number of cats in a row.

        cat = Cat(self)
        cat_width, cat_height = cat.rect.size

        available_space_x = self.settings.screen_width - (2 * cat_width)
        number_cats_x = available_space_x // cat_width

        """Specifies the number of rows to fit on the screen."""
        mouse_height = self.mouse.rect.height
        available_space_y = (self.settings.screen_height - (3 * cat_height) - mouse_height)
        number_rows = available_space_y // cat_height

        for row_number in range(number_rows):
            for cat_number in range(number_cats_x):
                self._create_cat(cat_number, row_number)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.mouse.moving_right = True

        elif event.key == pygame.K_LEFT:
            self.mouse.moving_left = True

        elif event.key == pygame.K_UP:
            self.mouse.moving_up = True

        elif event.key == pygame.K_DOWN:
            self.mouse.moving_down = True

        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.mouse.moving_right = False

        elif event.key == pygame.K_LEFT:
            self.mouse.moving_left = False

        elif event.key == pygame.K_UP:
            self.mouse.moving_up = False

        elif event.key == pygame.K_DOWN:
            self.mouse.moving_down = False

    def _check_events(self):
        """Handles key and mouse presses."""
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mous_pos = pygame.mouse.get_pos()
                self._check_play_button(mous_pos)

    def _change_fleet_direction(self):
        """Lowers the entire fleet and changes its direction."""
        for cat in self.cats.sprites():
            cat.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_fleet_edges(self):
        """Reacts when the cat reaches the edge of the screen."""
        for cat in self.cats.sprites():
            if cat.check_edges():
                self._change_fleet_direction()
                break

    def _fire_bullet(self):
        """Creating a new projectile and including it in the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _check_bullet_cat_collisions(self):
        """Handling collisions of shells with cats."""
        collisions = pygame.sprite.groupcollide(self.bullets, self.cats, True, True)

        if collisions:
            for cats in collisions.values():
                self.stats.score += self.settings.cat_points * len(cats)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

        if not self.cats:
            # Destruction of existing bullets and the creation of a new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.scoreboard.prep_level()

    def _check_cats_bottom(self):
        """Checks if the cats have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for cat in self.cats.sprites():
            if cat.rect.bottom >= screen_rect.bottom:
                self.mouse.display_RIP()
                self._update_screen()
                self.mouse.display_mouse()

                self._mouse_hit()

                break

    def reset_stats(self):
        self.stats.reset_stats()
        self.stats.game_active = True
        self.scoreboard.prep_score()
        self.scoreboard.prep_level()
        self.scoreboard.prep_mice()

    def clean_sprites(self):
        self.cats.empty()
        self.bullets.empty()

    def _check_play_button(self, mouse_pos):
        """Starts a new game when the Play button is pressed."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.stats.game_active:
            # Reset game settings.
            self.settings.initialize_dynamic_settings()

            # Reset game statistics.
            self.reset_stats()

            # Cleaning lists of cats and projectiles
            self.clean_sprites()

            # Create a new fleet and place the mouse in the center.
            self._create_fleet()
            self.mouse.center_mouse()

            # The mouse pointer is hidden.
            pygame.mouse.set_visible(False)

    def _update_bullets(self):
        """Updates projectile positions and destroys old projectiles."""

        """ Checking hits on cats. If a hit is detected, remove the projectile and the cat
        Generally speaking, there should have been a method for determining the intersection of several rectangles, 
        but pygame has its own groupcollide() method which adds the key-value pair to the returned dictionary every 
        time between the projectile rectangle and cat an overlap is detected."""

        # Update projectile positions.
        self.bullets.update()

        # Removing projectiles that have gone off the edge of the screen.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_cat_collisions()

    def _update_screen(self):
        """Updates the images on the screen and displays the new screen."""
        self.screen.blit(self.background, (0, 0))
        self.mouse.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.cats.draw(self.screen)

        self.scoreboard.show_score()

        # The Play button is displayed if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Display the last rendered screen.
        pygame.display.flip()

    def _update_cats(self):
        """Checks if the cat has reached the edge of the screen,
         with the subsequent update of the positions of all cats in the fleet"""
        self._check_fleet_edges()
        self.cats.update()

        # Check for cat-mouse collisions.
        if pygame.sprite.spritecollideany(self.mouse, self.cats):
            self.mouse.display_RIP()
            self._update_screen()
            self.mouse.display_mouse()

            self._mouse_hit()

        # Check if the cats have reached the bottom of the screen.
        self._check_cats_bottom()

    def run(self):
        """Launching the main game loop."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.mouse.update()
                self._update_bullets()
                self._update_cats()

            self._update_screen()


if __name__ == '__main__':
    game = CatInvasion()
    game.run()
