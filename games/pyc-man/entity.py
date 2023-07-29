# configuration for all entities in the game

import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from random import randint


class Entity(object):
    def __init__(self, node):
        self.name = None
        self.directions = {UP: Vector2(0, -1), DOWN: Vector2(0, 1),
                           LEFT: Vector2(-1, 0), RIGHT: Vector2(1, 0), STOP: Vector2()}
        self.direction = STOP
        self.set_speed(100)
        self.radius = 10
        self.collide_radius = 5
        self.color = WHITE  # default
        self.visible = True
        self.disable_portal = False
        self.goal = None
        self.direction_method = self.random_direction
        self.set_start_node(node)
        self.image = None

    def set_position(self):
        """
        Set the position of the entity
        """
        self.position = self.node.position.copy()

    def update(self, dt):
        """
        Update the entity
        """
        self.position += self.directions[self.direction] * self.speed * dt

        if self.overshot_target():
            self.node = self.target
            directions = self.valid_directions()
            direction = self.direction_method(directions)

            if not self.disable_portal:
                if self.node.neighbors[PORTAL] is not None:
                    self.node = self.node.neighbors[PORTAL]

            self.target = self.get_new_target(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.get_new_target(self.direction)

            self.set_position()

    def get_valid_directions(self, direction):
        """
        Checks to see if directions are valid
        """
        if direction is not STOP:
            if self.name in self.node.access[direction]:
                if self.node.neighbors[direction] is not None:
                    return True
        return False

    def get_new_target(self, direction):
        """
        Get the new target
        """
        if self.get_valid_directions(direction):
            return self.node.neighbors[direction]
        return self.node

    def overshot_target(self):
        """
        Checks to see if the entity has overshot the target
        """
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node_to_target = vec1.magnitude_squared()
            node_to_self = vec2.magnitude_squared()
            return node_to_self >= node_to_target
        return False

    def reverse_direction(self):
        """
        Reverse the direction of the entity
        """
        self.direction *= -1
        temp_target = self.node
        self.node = self.target
        self.target = temp_target

    def opposite_direction(self, direction):
        """
        Checks to see if the direction is opposite
        """
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

    def valid_directions(self):
        """
        Checks to see if the direction is valid
        """
        valid = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.get_valid_directions(key):
                if key != self.direction * -1:
                    valid.append(key)
        if len(valid) == 0:
            valid.append(self.direction * -1)
        return valid

    def random_direction(self, directions):
        """
        Get a random direction
        """
        return directions[randint(0, len(directions) - 1)]

    def goal_direction(self, directions):
        """
        Get the goal direction
        """
        dist = []
        for direction in directions:
            vec = self.node.position + self.directions[direction] * TILEWIDTH - self.goal
            dist.append(vec.magnitude_squared())
        index = dist.index(min(dist))
        return directions[index]

    def set_start_node(self, node):
        """
        Set the starting node for entity
        """
        self.node = node
        self.start_node = node
        self.target = node
        self.set_position()

    def set_between_nodes(self, direction):
        """
        Set the node between nodes
        """
        if self.node.neighbors[direction] is not None:
            self.target = self.node.neighbors[direction]
            self.position = (self.node.position + self.target.position) / 2.0

    def reset(self):
        """
        Resets the entity
        """
        self.set_start_node(self.start_node)
        self.direction = STOP
        self.speed = 100
        self.visible = True

    def set_speed(self, speed):
        """
        Set the speed of the entity
        """
        self.speed = speed * TILEWIDTH / 16

    def render(self, screen):
        """
        Render the entity
        """
        if self.visible:
            if self.image is not None:
                adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
                p = self.position - adjust
                screen.blit(self.image, p.as_tuple())
            else:
                p = self.position.as_int()
                pygame.draw.circle(screen, self.color, p, self.radius)
