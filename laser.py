import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_settings, screen, ship):
        """Creates bullet object at ships current position"""
        super(Bullet, self).__init__()
        self.screen = screen

        #Create a bullet rect at (0,0) then set correct position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        #store bullets position as a decimal value
        self.y = float(self.rect.y)

        #update bullet color
        self.color = ai_settings.bullet_color
        self.bullet_speed_factor = ai_settings.bullet_speed_factor

    def draw_bullet(self):
        """draws bullet to screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)

    def update(self):
        """move bullet up the screen"""
        #update the decimal position of the bullet
        self.y -= self.bullet_speed_factor
        #update rect position
        self.rect.y = self.y


