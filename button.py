import pygame.font

class Button():
    def __init__(self, ai_settings, screen, message):
        """"Initialize button attriburttes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        #Set the dimensions and proporties of the button
        self.width, self.height = 200, 50
        self.button_color = (200, 0, 20)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #Build the buttons rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #The button message needs to be prepped only once
        self.prep_message(message)

    def prep_message(self, message):
        """"Turn message into a rendered image and center text on the button"""
        self.message_image = self.font.render(message, True, self.text_color, self.button_color)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center

    def draw_button(self):
        #Draw a blank button then draw a message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)