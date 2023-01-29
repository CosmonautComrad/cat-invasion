import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from cat import Cat


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализирует игру и создаёт игровые ресурсы."""
        pygame.init()
        self.settings = Settings()

        """Код для запуска в полноэкранном режиме"""
        """self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height"""

        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.cats = pygame.sprite.Group()

        self._create_fleet()

    def _create_cat(self, cat_number, row_number):
        # Создание кота и размещение его в ряду
        cat = Cat(self)
        cat_width, cat_height = cat.rect.size
        cat.x = cat_width + cat_width * cat_number
        cat.rect.x = cat.x
        cat.rect.y = cat.rect.height + cat.rect.height * row_number

        self.cats.add(cat)

    def _create_fleet(self):
        """Создание котофлота вторжения"""
        # Создание кота и вычисление количества котов в ряду.
        # Интервал между соседними котами равен половине ширины кота
        cat = Cat(self)
        cat_width, cat_height = cat.rect.size

        available_space_x = self.settings.screen_width - (2 * cat_width)
        number_cats_x = available_space_x // cat_width

        """Определяет количество рядов, помещающихся на экране."""
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * cat_height) - ship_height)
        number_rows = available_space_y // cat_height

        # Создание котофлота вторжения.
        for row_number in range(number_rows):
            for cat_number in range(number_cats_x):
                self._create_cat(cat_number, row_number)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        elif event.key == pygame.K_UP:
            self.ship.moving_up = True

        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True

        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

        elif event.key == pygame.K_UP:
            self.ship.moving_up = False

        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _check_events(self):
        """Обрабатывает нажатия клавиш и мыши."""
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _change_fleet_direction(self):
        """Опускает весь котофлот и меняет его направление"""
        for cat in self.cats.sprites():
            cat.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_fleet_edges(self):
        """Реагирует на достижение котом края экрана."""
        for cat in self.cats.sprites():
            if cat.check_edges():
                self._change_fleet_direction()
                break

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды."""
        # Обновление позиций снарядов.
        self.bullets.update()

        # Удаление снарядов, вышедших за край экрана.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Проверка попаданий в котов.
        # При обнаружении попадания удалить снаряд и кота
        collisions = pygame.sprite.groupcollide(self.bullets, self.cats, True, True)

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.cats.draw(self.screen)

        # Отображение последнего прорисованного экрана.
        pygame.display.flip()

    def _update_cats(self):
        """Проверяет, достиг ли кот края экрана,
        с последующим обновлением позиций всех котов во флоте"""
        self._check_fleet_edges()
        self.cats.update()

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_cats()
            self._update_screen()


if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
