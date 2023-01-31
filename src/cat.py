import pygame
from pygame.sprite import Sprite


class Cat(Sprite):
    """A class representing a single cat."""

    def __init__(self, game):
        """Initializes the cat and sets its initial position"""
        super().__init__()

        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.image.load('..//recources/images/cat.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width / 10
        self.rect.y = self.rect.height / 10

        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right > screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Moves the cat."""
        self.x += (self.settings.cat_speed_factor * self.settings.fleet_direction)
        self.rect.x = self.x
