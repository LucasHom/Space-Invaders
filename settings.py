class Settings():
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the games settings"""
        #settings for the screen
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (10, 10, 10)

        #ship settings
        self.ship_limit = 3

        #bullet settings
        self.bullet_width = 1920
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5
        self.destroy_single_ship = True

        #alien settings
        self.fleet_drop_speed = 10

        #How quickly the game speeds up
        self.speed_up_scale = 1.1

        #How much alien values increase by
        self.alien_value_scale = 1.5

        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        """"Initialize settings that change throughout the game"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        #Fleet direction of 1 represents moving right; -1 means moving left
        self.fleet_direction = 1

        #scoring
        self.alien_value = 50

    def increase_speed(self):
        """Increase speed settings and alien point values"""
        self.ship_speed_factor *= self.speed_up_scale
        self.bullet_speed_factor *= self.speed_up_scale
        self.alien_speed_factor *= self.speed_up_scale

        self.alien_value = int(self.alien_value_scale * self.alien_value)
        print(self.alien_value)