class Settings:
    """Class for settings of Cat Invasion."""

    def __init__(self):
        """Initialize settings"""

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.sky_color = (198, 154, 251)

        # Mouse settings
        self.mouse_limit = 3

        # Settings of bullet
        self.bullet_width = 4
        self.bullet_height = 12
        self.bullet_color = (0, 0, 0)
        self.bullets_allowed = 8

        # Settings of cats
        self.fleet_drop_speed = 15

        # Game acceleration rate
        self.speedup_scale = 1.1

        # Growth rate of the cost of cats
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initializes dynamic settings."""
        self.mouse_speed_factor = 1.5
        self.bullet_speed_factor = 3.0
        self.cat_speed_factor = 1.0
        self.fleet_direction = 1
        self.cat_points = 50

    def increase_speed(self):
        """Increases cat speed and cost settings."""
        self.mouse_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.cat_speed_factor *= self.speedup_scale

        self.cat_points = int(self.cat_points * self.score_scale)



