import pygame.font
from pygame.sprite import Group

from mouse import Mouse


class Scoreboard:
    """Class for displaying game information."""

    def __init__(self, game):
        """Initializes the scoring attributes."""
        self.game = game

        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats

        self.text_color = (30, 30, 30)
        self.high_score_color = (255, 0, 0)
        self.level_text_color = (0, 0, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_mice()

    def prep_score(self):
        """Converts score to image."""
        rounder_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounder_score)

        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.sky_color)

        # Вывод счета в правой верхней части экрана.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """"Converts highest score to image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)

        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.high_score_color, self.settings.sky_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Converts current level to image."""
        level_str = str(f"Level: {self.stats.level}")
        self.level_image = self.font.render(level_str, True,
                                            self.level_text_color, self.settings.sky_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_mice(self):
        """Number of mice left."""
        self.mice = Group()

        for mouse_number in range(self.stats.mice_left):
            mouse = Mouse(self.game)
            mouse.rect.x = 10 + mouse_number * mouse.rect.width
            mouse.rect.y = 10
            self.mice.add(mouse)

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.mice.draw(self.screen)
