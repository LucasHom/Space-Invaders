import sys

import pygame

from laser import Bullet

from alien import Alien

from time import sleep

#check for changes

def check_events(stats, button, ai_settings, screen, ship, aliens, bullets, sb):
    """Watch for keyboard and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, ship, aliens, bullets, stats, button, mouse_x, mouse_y, sb)

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, stats, aliens, sb)
        elif event.type == pygame.KEYUP:
            check_keyup_events(ship, event)

def check_keydown_events(event, ai_settings, screen, ship, bullets, stats, aliens, sb):
        if not stats.active and event.key == pygame.K_SPACE:
            game_setup(ai_settings, screen, ship, aliens, bullets, stats, sb)

        elif event.key == pygame.K_RIGHT:
            ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            fire_bullet(ai_settings, bullets, screen, ship)
        elif event.key == pygame.K_ESCAPE:
            sys.exit()


def game_setup(ai_settings, screen, ship, aliens, bullets, stats, sb):
    stats.reset_stats()
    sb.prep_score()
    #sb.prep_highscore()
    sb.prep_level()
    sb.prep_lives()
    stats.active = True
    pygame.mouse.set_visible(False)

    # empty the list of aliens and bullets
    aliens.empty()
    bullets.empty()

    # Create a new fleet and center the ship
    create_fleet(ai_settings, screen, aliens, ship)
    ship.center_ship()

def check_play_button(ai_settings, screen, ship, aliens, bullets, stats, button, mouse_x, mouse_y, sb):
    """"Start a new game when the player hits play"""
    button_clicked = button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.active:
        ai_settings.init_dynamic_settings()
        game_setup(ai_settings, screen, ship, aliens, bullets, stats, sb)
        stats.level = 1


def check_keyup_events(ship, event):
        if event.key == pygame.K_RIGHT:
            ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            ship.moving_left = False

def ship_hit(ai_settings, gs, screen, ship, aliens, bullets, sb):
    """"Responds to a ship being hit by an alien"""
    #Decrement ships left
    if gs.ships_left > 0:
        gs.ships_left -= 1

        #change lives graphic
        sb.prep_lives()

        #Empty the list of bullets and aliens
        bullets.empty()
        aliens.empty()

        #Create a new fleet and center the ship
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()

        #pause

        sleep(0.5)
    else:
        gs.active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """"Check if any aliens have reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #Treat same as if ship got hit
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
            break

def update_screen(ai_settings, gs, screen, ship, bullets, aliens, button, sb):
    """Set screen settings and draws ship/alien"""
    screen.fill(ai_settings.bg_color)
    #redraw all bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    #Draw scoreboard to the screen
    sb.display_score()

    #Draw the play button if the game is inactive
    if gs.active == False:
        button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()

def fire_bullet(ai_settings, bullets, screen, ship):
    # Create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        bullet = Bullet(ai_settings, screen, ship)
        bullets.add(bullet)

def update_bullets(ai_settings, bullets, aliens, screen, ship, gs, sb):
    """"Update position of bullets and get rid of old bullets"""
    bullets.update()

    # get rid of bullets off screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_collision(ai_settings, aliens, bullets, screen, ship, gs, sb)

def check_bullet_collision(ai_settings, aliens, bullets, screen, ship, gs, sb):
    #Check for any bullets that have hit aliens
    #If so get rid of the bullet and the alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, ai_settings.destroy_single_ship, True)

    if collisions:
        for aliens in collisions.values():
            gs.score += ai_settings.alien_value * len(aliens)
            sb.prep_score()

        check_highscores(gs, sb)

    if len(aliens) == 0:
        #Destroy existing bullets and create new fleet
        bullets.empty()
        #Increase game speed
        ai_settings.increase_speed()
        #prep and increase level
        gs.level += 1
        sb.prep_level()
        # Add wait here
        create_fleet(ai_settings, screen, aliens, ship)

def create_fleet(ai_settings, screen, aliens, ship):
    """Create a full fleet of aliens"""
    #Create an alien and find the number of aliens in a row.
    #Note: Spacing between each alien is = one alien width
    alien = Alien(screen, ai_settings)
    alien_width = alien.rect.width
    num_aliens_x = get_num_aliens_x(ai_settings, alien_width)
    num_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    #Create a fleet of aliens
    for row in range(num_rows):
        for alien_num in range(num_aliens_x):
            #Create an alien and place it in the row
            create_alien(ai_settings, screen, aliens, alien_num, row)

def get_num_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row"""
    alien_space_x = ai_settings.screen_width - alien_width * 2
    num_aliens_x = int(alien_space_x / (alien_width * 2))
    return num_aliens_x

def create_alien(ai_settings, screen, aliens, alien_num, row_num):
    """"Create an alien and place it in the row"""
    alien = Alien(screen, ai_settings)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_num
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_num
    aliens.add(alien)

def get_number_rows(ai_settings, ship_height, alien_height):
    """"Determine the number of rows of alien ships that fit on the screen"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    num_rows = int(available_space_y / (2 * alien_height))
    return num_rows

def update_aliens(ai_settings, aliens, ship, gs, screen, bullets, sb):
    """"Update the positions of all aliens in the fleet"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings,gs ,screen ,ship, aliens, bullets, sb)
    #Look for alien hitting bottom of screen
    check_aliens_bottom(ai_settings, gs, screen, ship, aliens, bullets, sb)


def check_fleet_edges(ai_settings, aliens):
    """"Respond appropriately if any aliens have hit the edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            #Change fleet direction
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """"Dropping the entire fleet and changing the fleets direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed

    ai_settings.fleet_direction *= -1

def check_highscores(stats, sb):
    """Check to see if there is a new highscore"""
    if stats.score > stats.highscore:
        stats.highscore = stats.score
        sb.prep_highscore()