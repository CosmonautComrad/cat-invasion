import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from button import Button
from mouse import Mouse
from bullet import Bullet
from cat import Cat


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализирует игру и создаёт игровые ресурсы."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height))

        self.background = pygame.image.load("E:/cat-invasion/recources/images/BG.png").convert()
        pygame.display.set_caption("Cat Invasion")

        # Создание экземпляра для хранения игровой статистики.
        self.stats = GameStats(self)

        self.mouse = Mouse(self)
        self.bullets = pygame.sprite.Group()
        self.cats = pygame.sprite.Group()

        self._create_fleet()

        # Создание кнопки Play
        self.play_button = Button(self, "Play")

    def _mouse_hit(self):
        """Обрабатывает столкновение мыши с котом."""

        if self.stats.mice_left > 0:

            self.stats.mice_left -= 1

            # Очистка списков котов и снарядов.
            self.cats.empty()
            self.bullets.empty()

            # Создание нового флота и размещение мыши в центре.
            self._create_fleet()
            self.mouse.center_mouse()

            sleep(2)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

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
        mouse_height = self.mouse.rect.height
        available_space_y = (self.settings.screen_height - (3 * cat_height) - mouse_height)
        number_rows = available_space_y // cat_height

        # Создание котофлота вторжения.
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
        """Обрабатывает нажатия клавиш и мыши."""
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

    def _check_bullet_cat_collisions(self):
        """Обработка коллизий снарядов с котами."""
        collisions = pygame.sprite.groupcollide(self.bullets, self.cats, True, True)

        if not self.cats:
            # Уничтожение существующих снарядов и создание нового флота.
            self.bullets.empty()
            self._create_fleet()

    def _check_cats_bottom(self):
        """Проверяет, добрались ли коты до нижнего края экрана"""
        screen_rect = self.screen.get_rect()
        for cat in self.cats.sprites():
            if cat.rect.bottom >= screen_rect.bottom:
                # Происходит то же, что и при столкновении с кораблем.
                self._mouse_hit()
                break

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Сброс игровой статистики.
            self.stats.reset_stats()
            self.stats.game_active = True

            # Очистка списков котов и снарядов
            self.cats.empty()
            self.bullets.empty()

            # Создание нового флота и размещение мыша в центре.
            self._create_fleet()
            self.mouse.center_mouse()

            # Указатель мыши скрывается.
            pygame.mouse.set_visible(False)

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды."""

        """ Проверка попаданий в котов. При обнаружении попадания удалить снаряд и кота
            Вообще говоря, тут должен был быть метод для определения пересечения нескольких прямоугольников, но у
            pygame есть свой метод groupcollide(), который каждый раз, когда между прямоугольником снаряда 
            и кота обнаруживается перекрытие,  добавляет пару «ключ-значение» в возвращаемый словарь."""

        # Обновление позиций снарядов.
        self.bullets.update()

        # Удаление снарядов, вышедших за край экрана.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_cat_collisions()

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        self.screen.blit(self.background, (0, 0))
        self.mouse.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.cats.draw(self.screen)

        # Кнопка Play отображается в том случае, если игра неактивна.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Отображение последнего прорисованного экрана.
        pygame.display.flip()

    def _update_cats(self):
        """Проверяет, достиг ли кот края экрана,
        с последующим обновлением позиций всех котов во флоте"""
        self._check_fleet_edges()
        self.cats.update()

        # Проверка коллизий "кот - мыш".
        if pygame.sprite.spritecollideany(self.mouse, self.cats):
            self.mouse.display_RIP()
            self._update_screen()
            self.mouse.display_mouse()
            self._mouse_hit()

        # Проверка, добрались ли коты до нижнего края экрана.
        self._check_cats_bottom()

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.mouse.update()
                self._update_bullets()
                self._update_cats()

            self._update_screen()


if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
