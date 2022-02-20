import pygame.font

from pygame.sprite import Group

from ship import Ship

class Scoreboard():
    """A class to report scoring information"""
    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Font settings for scoreboard
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()

        self.prep_highscore()

        self.prep_level()

        self.prep_lives()

    def prep_score(self):
        """Turns the score into an image"""
        rounded_score = int(round(self.stats.score, -1))

        score_string = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_string, True, self.text_color, self.ai_settings.bg_color)

        #Displays the score at the top right of the screen
        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.right = self.screen_rect.right - 20
        self.score_image_rect.top = 20

    def prep_highscore(self):
        """Turns highscore into an image"""

        rounded_score = int(round(self.stats.highscore, -1))

        score_string = "High Score: {:,}".format(rounded_score)
        self.highscore_image = self.font.render(score_string, True, self.text_color, self.ai_settings.bg_color)

        # Displays the score at the top of the screen
        self.highscore_image_rect = self.highscore_image.get_rect()
        self.highscore_image_rect.centerx = self.screen_rect.centerx
        self.highscore_image_rect.top = self.score_image_rect.top

    def prep_level(self):
        """Turns level number into an image"""

        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)

        #Displays the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_image_rect.right
        self.level_rect.top = 60

    def prep_lives(self):
        """Display how many ships remaining"""
        self.ships = Group()
        for ship_num in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_num * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)



    def display_score(self):
        """"Displays message to the screen"""
        self.screen.blit(self.score_image, self.score_image_rect)
        self.screen.blit(self.highscore_image, self.highscore_image_rect)
        self.screen.blit(self.level_image, self.level_rect)
        #Draw ships
        self.ships.draw(self.screen)
