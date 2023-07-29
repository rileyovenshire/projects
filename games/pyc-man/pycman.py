# PyGame clone of Pacman, using PyGame

import pygame
from pygame.locals import *
from constants import *
from vector import Vector2
from entity import Entity
from sprites import PycmanSprites
from random import randint


class Pycman(Entity):
    def __init__(self, node):
        Entity.__init__(self, node )
        self.name = PYCMAN
        self.color = YELLOW
        self.direction = LEFT
        self.set_between_nodes(LEFT)
        self.alive = True
        self.sprites = PycmanSprites(self)

    def reset(self):
        """
        Reset the Pycman object
        """
        Entity.reset(self)
        self.direction = LEFT
        self.set_between_nodes(LEFT)
        self.alive = True
        self.image = self.sprites.get_start_image()
        self.sprites.reset()

    def die(self):
        """
        Pycman dies, RIP.
        """
        self.alive = False
        self.direction = STOP

    def update(self, dt):
        """
        Update the Pycman object
        """
        self.sprites.update(dt)
        self.position += self.directions[self.direction] * self.speed * dt
        direction = self.get_valid_key()
        if self.overshot_target():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.get_new_target(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.get_new_target(self.direction)

            if self.target is self.node:
                self.direction = STOP

            self.set_position()

        else:
            if self.opposite_direction(direction):
                self.reverse_direction()


    def get_valid_key(self):
        """
        Get the valid key
        """
        pressed = pygame.key.get_pressed()
        if pressed[K_UP]:
            return UP
        if pressed[K_DOWN]:
            return DOWN
        if pressed[K_LEFT]:
            return LEFT
        if pressed[K_RIGHT]:
            return RIGHT
        return STOP

    def eat_pellets(self, pellets):
        """
        Eat the pellets
        """
        for pellet in pellets:
            if self.collision(pellet):
                return pellet
        return None

    def collide_ghost(self, ghost):
        """
        Collide with the ghost
        """
        return self.collision(ghost)

    def collision(self, entity):
        """
        Check for collision with another entity
        """
        distance = self.position - entity.position
        distance_squared = distance.magnitude_squared()
        radii_squared = (self.collide_radius + entity.collide_radius) ** 2
        if distance_squared <= radii_squared:
            return True
        return False
