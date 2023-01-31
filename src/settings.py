class Settings:
    """Класс для хранения настроек игры Cat Invasion."""

    def __init__(self):
        """Инициализирует настройки игры."""

        # Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800

        # Параметры мыши
        self.mouse_speed = 1.5
        self.mouse_limit = 3

        # Параметры снаряда
        self.bullet_speed = 2
        self.bullet_width = 4
        self.bullet_height = 12
        self.bullet_color = (0, 0, 0)
        self.bullets_allowed = 8

        # Настройки котов
        self.cat_speed = 1.0
        self.fleet_drop_speed = 15
        self.fleet_direction = 1
