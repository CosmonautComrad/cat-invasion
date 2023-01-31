import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class for controlling projectiles fired by the mouse."""

    def __init__(self, game):
        """Creates a projectile object at the current mouse position."""
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        # Creating a projectile at position (0, 0) and assigning the correct position.
        self.image = pygame.image.load("..//recources/images/bullet.png")
        self.rect = self.image.get_rect()

        self.rect.midtop = game.mouse.rect.midtop

        self.y = float(self.rect.y)

    def update(self):
        """Moves the projectile up the screen."""
        self.y -= self.settings.bullet_speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        self.screen.blit(self.image, self.rect)

    """def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)"""