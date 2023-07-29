# configuration for all pellets in the game

import pygame
from vector import Vector2
from constants import *
import numpy as np

class Pellet(object):
    def __init__(self, row, column):
        self.name = PELLET
        self.position = Vector2(column*TILEWIDTH, row*TILEHEIGHT)
        self.color = WHITE
        self.radius = int(2 * TILEWIDTH / 16)
        self.collide_radius = 2 * TILEWIDTH / 16
        self.points = 10
        self.visible = True

    def render(self, screen):
        """
        Renders the pellet.
        """
        if self.visible:
            adjustment = Vector2(int(TILEWIDTH/2), int(TILEHEIGHT/2))
            pos = self.position + adjustment
            pygame.draw.circle(screen, self.color, pos.as_int(), self.radius)

class PowerPellet(Pellet):
    def __init__(self, row, column):
        Pellet.__init__(self, row, column)
        self.name = POWERPELLET
        self.radius = int(8 * TILEWIDTH / 16)
        self.points = 50
        self.flash_time = 0.2
        self.timer = 0

    def update(self, dt):
        """
        Update the power pellet
        """
        self.timer += dt
        if self.timer >= self.flash_time:
            self.visible = not self.visible
            self.timer = 0

class PelletGroup(object):
    def __init__(self, pelletfile):
        self.pellet_list = []
        self.powerpellet_list = []
        self.create_pellet_list(pelletfile)
        self.num_eaten = 0

    def update(self, dt):
        """
        Update the pellet group
        """
        for powerpellet in self.powerpellet_list:
            powerpellet.update(dt)

    def create_pellet_list(self, pelletfile):
        """
        Creates a list of pellets from a file
        """
        data = self.read_pellet_file(pelletfile)
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in ['.', '+']:
                    self.pellet_list.append(Pellet(row, col))
                elif data[row][col] in ['P', 'p']:
                    powerpellet = PowerPellet(row, col)
                    self.powerpellet_list.append(powerpellet)
                    self.pellet_list.append(powerpellet)

    def read_pellet_file(self, pelletfile):
        """
        Reads the pellet file
        """
        return np.loadtxt(pelletfile, dtype='<U1')

    def is_empty(self):
        """
        Checks if the pellet group is empty
        """
        if len(self.pellet_list) == 0:
            return True
        else:
            return False


    def render(self, screen):
        """
        Renders the pellet group
        """
        for pellet in self.pellet_list:
            pellet.render(screen)

