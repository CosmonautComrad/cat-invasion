class Settings:
    """Класс для хранения настроек игры Alien Invasion."""

    def __init__(self):
        """Инициализирует настройки игры."""
        # Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (72, 61, 139)

        # Параметры корабля
        self.ship_speed = 1.5
        self.ship_limit = 3

        # Параметры снаряда
        self.bullet_speed = 2
        self.bullet_width = 4
        self.bullet_height = 12
        self.bullet_color = (0, 0, 0)
        self.bullets_allowed = 8

        # Настройки котов
        self.cat_speed = 1.0
        self.fleet_drop_speed = 15
        # fleet_direction = 1 это движение вправо; а -1 - влево.
        self.fleet_direction = 1
