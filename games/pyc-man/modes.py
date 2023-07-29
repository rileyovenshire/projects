# configures modes for the game

from constants import *


class MainMode(object):
    def __init__(self):
        self.timer = 0
        self.scatter()

    def update(self, dt):
        """
        Update the mode
        """
        self.timer += dt
        if self.timer >= self.time:
            if self.mode is SCATTER:
                self.chase()
            elif self.mode is CHASE:
                self.scatter()

    def scatter(self):
        """
        Set the mode to scatter
        """
        self.mode = SCATTER
        self.time = 7
        self.timer = 0

    def chase(self):
        """
        Set the mode to chase
        """
        self.mode = CHASE
        self.time = 20
        self.timer = 0


class ModeController(object):
    def __init__(self, entity):
        self.timer = 0
        self.time = None
        self.main_mode = MainMode()
        self.current = self.main_mode.mode
        self.entity = entity

    def update(self, dt):
        """
        Update the mode
        """
        self.main_mode.update(dt)
        if self.current is FRIGHT:
            self.timer += dt
            if self.timer >= self.time:
                self.time = None
                self.entity.normalMode()
                self.current = self.main_mode.mode
        elif self.current in [SCATTER, CHASE]:
            self.current = self.main_mode.mode

        if self.current is SPAWN:
            if self.entity.node == self.entity.spawn_node:
                self.entity.normal_mode()
                self.current = self.main_mode.mode

    def set_fright_mode(self):
        """
        Set the mode to fright
        """
        if self.current in [SCATTER, CHASE]:
            self.timer = 0
            self.time = 7
            self.current = FRIGHT
        elif self.current is FRIGHT:
            self.timer = 0

    def set_spawn_mode(self):
        """
        Set the mode to spawn
        """
        if self.current is FRIGHT:
            self.current = SPAWN
