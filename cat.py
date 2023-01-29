import pygame
from pygame.sprite import Sprite


class Cat(Sprite):
    """Класс представляющий одного кота"""

    def __init__(self, ai_game):
        """Инициализирует кота и задаёт его начальную позицию"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Загрузка изображения кота и назначение атрибута rect.
        self.image = pygame.image.load('images/cat.png')
        self.rect = self.image.get_rect()

        # Каждый новый кот появляется в левом верхнем углу экрана
        self.rect.x = self.rect.width / 10
        self.rect.y = self.rect.height / 10

        # Сохранение точной горизонтальной позиции пришельца.
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
