import pygame


class Mouse:
    """Класс для управления мышом"""

    def __init__(self, game):
        """Инициализирует мыш и задаёт его начальную позицию"""
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings

        self.mouse_image = pygame.image.load('E:/cat-invasion/recources/images/mouse.png')
        self.image = self.mouse_image
        self.rect = self.image.get_rect()

        self.dead_mouse = pygame.image.load('E:/cat-invasion/recources/images/RIP.png')

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
        """Обновляет позицию мыша с учётом флага"""

        # Обновляется атрибут x объекта mouse, не rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.mouse_speed

        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.mouse_speed

        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.mouse_speed

        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.mouse_speed

        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Рисует мыш в текущей позиции."""
        self.screen.blit(self.image, self.rect)

    def center_mouse(self):
        """Размещает мыш в центре нижней стороны."""

        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def display_RIP(self):
        """Меняет image на картинку с могилой"""
        self.image = self.dead_mouse

    def display_mouse(self):
        """Меняет обратно на картинку с мышой"""
        self.image = self.mouse_image