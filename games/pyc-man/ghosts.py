# ghost configuration for pycman

import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from modes import ModeController
from sprites import GhostSprites


class Ghost(Entity):
    def __init__(self, node, pycman=None, blinky=None):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2()
        self.direction_method = self.goal_direction
        self.pycman = pycman
        self.mode = ModeController(self)
        self.blinky = blinky
        self.home_node = node

    def reset(self):
        """
        Reset the ghost
        """
        Entity.reset(self)
        self.points = 200
        self.direction_method = self.goal_direction

    def update(self, dt):
        """
        Updates the ghost according to the current mode
        """
        self.sprites.update(dt)
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    def scatter(self):
        """
        Ghosts scatter to their home corners
        """
        self.goal = Vector2()

    def chase(self):
        """
        Ghosts chase pycman
        """
        self.goal = self.pycman.position

    def spawn(self):
        """
        Spawn the ghost
        """
        self.goal = self.spawn_node.position

    def set_spawn_node(self, node):
        """
        Sets ghost's spawn node
        """
        self.spawn_node = node

    def start_spawn(self):
        """
        Start the ghost's spawn
        """
        self.mode.set_spawn_mode()
        if self.mode.current == SPAWN:
            self.set_speed(150)
            self.direction_method = self.goal_direction
            self.spawn()

    def start_fright(self):
        """
        Puts ghost into fright mode
        """
        self.mode.set_fright_mode()
        if self.mode.current == FRIGHT:
            self.set_speed(75)
            self.direction_method = self.random_direction

    def normal_mode(self):
        """
        Returns ghost to normal mode
        """
        self.set_speed(100)
        self.direction_method = self.goal_direction
        self.home_node.deny_access(DOWN, self)


class Blinky(Ghost):
    def __init__(self, node, pycman=None, blinky=None):
        Ghost.__init__(self, node, pycman, blinky)
        self.name = BLINKY
        self.color = RED
        self.sprites = GhostSprites(self)


class Pinky(Ghost):
    def __init__(self, node, pycman=None, blinky=None):
        Ghost.__init__(self, node, pycman, blinky)
        self.name = PINKY
        self.color = PINK
        self.sprites = GhostSprites(self)

    def scatter(self):
        """
        Pinky scatters to the top left corner
        """
        self.goal = Vector2(TILEWIDTH * NCOLS, 0)

    def chase(self):
        """
        Pinky chases four tiles ahead of pycman
        """
        self.goal = self.pycman.position + self.pycman.directions[self.pycman.direction] * 4 * TILEWIDTH


class Inky(Ghost):
    def __init__(self, node, pycman=None, blinky=None):
        Ghost.__init__(self, node, pycman, blinky)
        self.name = INKY
        self.color = TEAL
        self.sprites = GhostSprites(self)

    def scatter(self):
        """
        Inky scatters to the top right corner
        """
        self.goal = Vector2(TILEWIDTH * NCOLS, TILEHEIGHT * NROWS)

    def chase(self):
        """
        Inky chases two tiles ahead of pycman
        """
        vector1 = self.pycman.position + self.pycman.directions[self.pycman.direction] * 2 * TILEWIDTH
        vector2 = (vector1 - self.blinky.position) * 2
        self.goal = self.blinky.position + vector2


class Clyde(Ghost):
    def __init__(self, node, pycman=None, blinky=None):
        Ghost.__init__(self, node, pycman, blinky)
        self.name = CLYDE
        self.color = ORANGE
        self.sprites = GhostSprites(self)

    def scatter(self):
        """
        Clyde scatters to the bottom left corner
        """
        self.goal = Vector2(0, TILEHEIGHT * NROWS)

    def chase(self):
        """
        Clyde chases pycman unless he is within 8 tiles
        """
        distance = self.pycman.position - self.position
        distance_squared = distance.magnitude_squared()
        if distance_squared <= 8 * TILEWIDTH ** 2:
            self.scatter()
        else:
            self.goal = self.pycman.position + self.pycman.directions[self.pycman.direction] * 4 * TILEWIDTH


class GhostGroup(object):
    def __init__(self, node, pycman):
        self.blinky = Blinky(node, pycman)
        self.pinky = Pinky(node, pycman)
        self.inky = Inky(node, pycman, self.blinky)
        self.clyde = Clyde(node, pycman)
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

    def __iter__(self):
        """
        Returns an iterator for the ghosts
        """
        return iter(self.ghosts)

    def update(self, dt):
        """
        Updates the ghosts
        """
        for ghost in self.ghosts:
            ghost.update(dt)

    def start_fright(self):
        """
        Puts all ghosts into fright mode
        """
        for ghost in self.ghosts:
            ghost.start_fright()
        self.reset_points()

    def reset_points(self):
        """
        Resets the points of all ghosts
        """
        for ghost in self.ghosts:
            ghost.points = 200

    def update_points(self):
        """
        Updates the points of all ghosts
        """
        for ghost in self.ghosts:
            ghost.points *= 2

    def set_spawn_node(self, node):
        """
        Sets the spawn node for all ghosts
        """
        for ghost in self.ghosts:
            ghost.set_spawn_node(node)

    def hide(self):
        """
        Hides all ghosts
        """
        for ghost in self.ghosts:
            ghost.visible = False

    def show(self):
        """
        Shows all ghosts
        """
        for ghost in self.ghosts:
            ghost.visible = True

    def reset(self):
        """
        Resets all ghosts
        """
        for ghost in self.ghosts:
            ghost.reset()

    def render(self, surface):
        """
        Renders all ghosts
        """
        for ghost in self.ghosts:
            ghost.render(surface)
