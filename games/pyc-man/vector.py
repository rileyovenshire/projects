# vector actions for the Pyc-Man game

import math


class Vector2(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.threshhold = 0.00001

    def add(self, other):
        """
        Adds one vector to another.
        """
        return Vector2(self.x + other.x, self.y + other.y)

    def sub(self, other):
        """
        Subtracts one vector from another.
        """
        return Vector2(self.x - other.x, self.y - other.y)

    def __neg__(self):
        """
        Returns the negative of the vector.
        """
        return Vector2(-self.x, -self.y)

    def __mul__(self, scalar):
        """
        Multiplies the vector by a scalar.
        """
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, other):
        """
        Divides the vector by a scalar.
        """
        return Vector2(self.x / float(other), self.y / float(other))

    def __eq__(self, other):
        """
        Checks if two vectors are equal.
        """
        if abs(self.x - other.x) < self.threshhold and abs(self.y - other.y) < self.threshhold:
            return True
        return False

    def magnitude_squared(self):
        """
        Returns the squared magnitude of the vector.
        """
        return self.x ** 2 + self.y ** 2

    def magnitude(self):
        """
        Returns the magnitude of the vector.
        """
        return math.sqrt(self.magnitude_squared())

    def __copy__(self):
        """
        Returns a copy of the vector.
        """
        return Vector2(self.x, self.y)

    def as_tuple(self):
        """
        Returns the vector as a tuple.
        """
        return (self.x, self.y)

    def as_int(self):
        """
        Returns the vector as a tuple of integers.
        """
        return (int(self.x), int(self.y))

    def __str__(self):
        """
        Returns the vector as a string.
        """
        return "Vector2({}, {})".format(self.x, self.y)