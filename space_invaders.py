import pygame

from pygame.sprite import Group

from settings import Settings

from ship import Ship

from alien import Alien

from game_stats import Gamestats

from button import Button

from scoreboard import Scoreboard

import game_functions as gf

def run_game():
    # Initialize game and creates a screen object
    pygame.init()
    pygame.display.set_caption("Aliens Attack!")
    game_icon = pygame.image.load("Images/galaga_ship.png")
    pygame.display.set_icon(game_icon)
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))


    #Create button
    message = "Start"
    button = Button(ai_settings, screen, message)




    #Make a ship, a group of aliens, and a group of bullets
    ship = Ship(ai_settings, screen)
    aliens = Group()
    #make a group to store bullets in
    bullets = Group()
    gs = Gamestats(ai_settings)

    #Initialize scoreboard
    sb = Scoreboard(ai_settings, screen, gs)

    #Create the fleet of aliens
    gf.create_fleet(ai_settings, screen, aliens, ship)

    #Start the main loop for the game.
    #icon = pygame.image.load('image.png')
    while True:
        gf.check_events(gs, button, ai_settings, screen, ship, aliens, bullets, sb)

        if gs.active == True:
            ship.update()
            gf.update_bullets(ai_settings, bullets, aliens, screen, ship, gs, sb)
            gf.update_aliens(ai_settings, aliens, ship, gs, screen, bullets, sb)

        gf.update_screen(ai_settings, gs, screen, ship, bullets, aliens, button, sb)





run_game()




