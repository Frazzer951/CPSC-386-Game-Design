class Settings():
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (150, 150, 150)
        self.laser_width = 2
        self.laser_height = 30
        self.laser_color = 255, 0, 0
        self.lasers_every = 10
        self.initialize_speed_settings()

    def initialize_speed_settings(self):
        self.ship_speed_factor = 3
        self.laser_speed_factor = 3

    def increase_speed(self):
        scale = self.speedup_scale
        self.ship_speed_factor *= scale
        self.laser_speed_factor *= scale
