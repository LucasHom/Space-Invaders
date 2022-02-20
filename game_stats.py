import game_functions as gf

class Gamestats():
    """"Tracks statistics for space invaders game"""
    def __init__(self, ai_settings):
        """"Initialize stats"""
        self.ai_settings = ai_settings
        self.reset_stats()
        
        #Highscore should never be reset
        self.highscore = gf.read_highscore()
        
        #Start space invaders in an inactive state until play button pressed
        self.active = False

        #level of game
        self.level = 1

    def reset_stats(self):
        """"Initialize stats that can chnage during the game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1



