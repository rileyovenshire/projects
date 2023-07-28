# Configuration file to run the application

import pygame
from pygame.locals import *
from constants import *


class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None

    def start_game(self):
        """
        Creates instance of the game.
        """
        self.set_background()

    def update(self):
        """
        Update the game
        """
        self.check_events()
        self.render()

    def set_background(self):
        """
        Set the background of the game
        """
        self.background = pygame.Surface(SCREENSIZE).convert
        self.background.fill(BLACK)

    def check_events(self):
        """
        Check for events
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

    def render(self):
        """
        Render the game
        """
        pygame.display.update()








# -------------------------------------------------
if __name__ == "__main__":
    game = GameController()
    game.start_game()
    while True:
        game.update()