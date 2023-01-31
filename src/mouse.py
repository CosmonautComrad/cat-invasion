import pygame


class Mouse:

    def __init__(self, game):
        """Initializes the mouse and sets its initial position."""
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings

        self.mouse_image = pygame.image.load('..//recources/images/mouse.png')
        self.image = self.mouse_image
        self.rect = self.image.get_rect()

        self.dead_mouse = pygame.image.load('..//recources/images/RIP.png')

        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def rotate(self, angle):
        return pygame.transform.rotate(self.image, angle)

    def update(self):
        """Updates the mouse position based on the flag."""

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.mouse_speed_factor

        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.mouse_speed_factor

        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.mouse_speed_factor

        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.mouse_speed_factor

        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Draws the mouse at the current position."""
        self.screen.blit(self.image, self.rect)

    def center_mouse(self):
        """Positions the mouse in the center of the bottom side."""

        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def display_RIP(self):
        """Changes image to an image with a grave."""
        self.image = self.dead_mouse

    def display_mouse(self):
        """Changes back to a picture with a mouse"""
        self.image = self.mouse_image