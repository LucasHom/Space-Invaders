import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Single alien in fleet"""
    def __init__(self, screen, ai_settings):
        """Initialize alien and set starting position"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #Load the alien image and set it's rect attribute
        self.image = pygame.image.load("Images/alien.bmp")
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()

        #Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #Store the aliens exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at it's current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """"Move the alien right or left"""
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """"Return true if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
