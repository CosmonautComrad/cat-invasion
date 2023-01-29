import pygame


class Ship:
    """Класс для управления кораблём"""

    def __init__(self, ai_game):
        """Инициализирует корабль и задаёт его начальную позицию"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Загружает изображение корабля и получает прямоугольник.
        self.mouse_image = pygame.image.load('images/mouse.png')
        self.image = self.mouse_image
        self.rect = self.image.get_rect()

        # Загружает изображение могилы
        self.dead_mouse = pygame.image.load('images/RIP.png')

        # Каждый новый корабль появляется у нижнего края экрана.
        self.rect.midbottom = self.screen_rect.midbottom

        # Сохранение вещественной координаты центра корабля.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Флаги перемещения
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def rotate(self, angle):
        return pygame.transform.rotate(self.image, angle)

    def update(self):
        """Обновляет позицию корабля с учётом флага"""
        # Обновляется атрибут x объекта ship, не rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed

        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        # Обновление атрибута rect на основании self.x
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Рисует мыш в текущей позиции."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
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