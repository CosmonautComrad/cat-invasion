class GameStats:
    """Stats tracking for Cat Invasion game."""

    def __init__(self, game):
        """Initializes statistics, keeps track of the state of the game."""
        self.settings = game.settings
        self.reset_stats()

        self.game_active = False

        self.high_score = 0

    def reset_stats(self):
        """Initializes statistics that change during the game."""
        self.mice_left = self.settings.mouse_limit
        self.score = 0
        self.level = 1