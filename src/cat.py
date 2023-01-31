import pygame
from pygame.sprite import Sprite


class Cat(Sprite):
    """Класс представляющий одного кота"""

    def __init__(self, game):
        """Инициализирует кота и задаёт его начальную позицию"""
        super().__init__()

        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.image.load('E:/cat-invasion/recources/images/cat.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width / 10
        self.rect.y = self.rect.height / 10

        self.x = float(self.rect.x)

    def check_edges(self):
        """Возвращает True, если кот находится у края экрана."""
        screen_rect = self.screen.get_rect()
        if self.rect.right > screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Перемещает кота вправо"""
        self.x += (self.settings.cat_speed * self.settings.fleet_direction)
        self.rect.x = self.x
