class GameStats:
    """Отслеживание статистики для игры Cat Invasion."""

    def __init__(self, game):
        """Инициализирует статистику"""
        self.settings = game.settings
        self.reset_stats()

        # Игра Cat Invasion запускается в неактивном состоянии.
        self.game_active = False

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.mice_left = self.settings.mouse_limit
