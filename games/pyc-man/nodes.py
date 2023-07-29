import pygame
from vector import Vector2
from constants import *
import numpy as np


class Node(object):
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.neighbors = {UP: None, DOWN: None, LEFT: None, RIGHT: None, PORTAL: None}
        self.access = {UP: [PYCMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT],
                       DOWN: [PYCMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT],
                       LEFT: [PYCMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT],
                       RIGHT: [PYCMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT]}

    def deny_access(self, direction, entity):
        """
        Denies access to a point for an entity
        """
        if entity.name in self.access[direction]:
            self.access[direction].remove(entity.name)

    def allow_access(self, direction, entity):
        """
        Allows access to a point for an entity
        """
        if entity.name not in self.access[direction]:
            self.access[direction].append(entity.name)

    def render(self, screen):
        """
        Render the node
        """
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                start = self.position.as_tuple()
                end = self.neighbors[n].position.as_tuple()
                pygame.draw.line(screen, WHITE, start, end, 4)
                pygame.draw.circle(screen, RED, self.position.as_int(), 12)


class NodeGroup(object):
    def __init__(self, level):
        self.level = level
        self.nodes_lookup_table = {}
        self.node_symbols = ['+', 'P', 'n']
        self.path_symbols = ['.', '-', '|', 'p']
        data = self.read_maze_file(level)
        self.create_node_table(data)
        self.connect_horizontally(data)
        self.connect_vertically(data)
        self.home_key = None

    def read_maze_file(self, level):
        """
        Read the maze file
        """
        return np.loadtxt(level, dtype='<U1')

    def create_node_table(self, data, x_off=0, y_off=0):
        """
        Creates a node lookup table
        """
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.node_symbols:
                    x, y = self.construct_key(col + x_off, row + y_off)
                    self.nodes_lookup_table[(x, y)] = Node(x, y)

    def construct_key(self, x, y):
        """
        Constructs a key for the node lookup table
        """
        return x * TILEWIDTH, y * TILEHEIGHT

    def connect_horizontally(self, data, x_off=0, y_off=0):
        """
        Connects nodes horizontally
        """
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.node_symbols:
                    if key is None:
                        key = self.construct_key(col + x_off, row + y_off)
                    else:
                        alt_key = self.construct_key(col + x_off, row + y_off)
                        self.nodes_lookup_table[key].neighbors[RIGHT] = self.nodes_lookup_table[alt_key]
                        self.nodes_lookup_table[alt_key].neighbors[LEFT] = self.nodes_lookup_table[key]
                        key = alt_key
                elif data[row][col] not in self.path_symbols:
                    key = None

    def connect_vertically(self, data, x_off=0, y_off=0):
        """
        Connects nodes vertically
        """
        data = data.transpose()
        for col in list(range(data.shape[0])):
            key = None
            for row in list(range(data.shape[1])):
                if data[col][row] in self.node_symbols:
                    if key is None:
                        key = self.construct_key(col + x_off, row + y_off)
                    else:
                        alt_key = self.construct_key(col + x_off, row + y_off)
                        self.nodes_lookup_table[key].neighbors[DOWN] = self.nodes_lookup_table[alt_key]
                        self.nodes_lookup_table[alt_key].neighbors[UP] = self.nodes_lookup_table[key]
                        key = alt_key
                elif data[col][row] not in self.path_symbols:
                    key = None

    def get_start_temp_node(self):
        """
        Get the start node
        """
        nodes = list(self.nodes_lookup_table.values())
        return nodes[0]

    def set_portal_pair(self, pairA, pairB):
        """
        Sets two sets of portals for the player to traverse
        """
        keyA = self.construct_key(*pairA)
        keyB = self.construct_key(*pairB)
        if keyA in self.nodes_lookup_table.keys() and keyB in self.nodes_lookup_table.keys():
            self.nodes_lookup_table[keyA].neighbors[PORTAL] = self.nodes_lookup_table[keyB]
            self.nodes_lookup_table[keyB].neighbors[PORTAL] = self.nodes_lookup_table[keyA]

    def create_home_nodes(self, x_off, y_off):
        """
        Creates home nodes for the ghosts
        """
        home_data = np.array(([['X', 'X', '+', 'X', 'X'],
                               ['X', 'X', '.', 'X', 'X'],
                               ['+', 'X', '.', 'X', '+'],
                               ['+', '.', '+', '.', '+'],
                               ['+', 'X', 'X', 'X', '+']]))
        self.create_node_table(home_data, x_off, y_off)
        self.connect_horizontally(home_data, x_off, y_off)
        self.connect_vertically(home_data, x_off, y_off)
        self.home_key = self.construct_key(x_off + 2, y_off)
        return self.home_key

    def connect_home_nodes(self, home_key, alt_key, direction):
        """
        Connects the home nodes to the rest of the maze
        """
        key = self.construct_key(*alt_key)
        self.nodes_lookup_table[home_key].neighbors[direction] = self.nodes_lookup_table[key]
        self.nodes_lookup_table[key].neighbors[direction * -1] = self.nodes_lookup_table[home_key]

    def get_node_from_pixels(self, x, y):
        """
        Allows the conversion of pixels to nodes
        """
        if (x, y) in self.nodes_lookup_table.keys():
            return self.nodes_lookup_table[(x, y)]
        else:
            return None

    def get_node_from_grid(self, col, row):
        """
        Allows the conversion of grid coordinates to nodes
        """
        x, y = self.construct_key(col, row)
        if (x, y) in self.nodes_lookup_table.keys():
            return self.nodes_lookup_table[(x, y)]
        else:
            return None

    def deny_access(self, col, row, direction, entity):
        """
        Denies access to a node for a given entity
        """
        node = self.get_node_from_grid(col, row)
        if node is not None:
            node.deny_access(direction, entity)

    def allow_access(self, col, row, direction, entity):
        """
        Allows access to a node for a given entity
        """
        node = self.get_node_from_grid(col, row)
        if node is not None:
            node.allow_access(direction, entity)

    def deny_access_list(self, col, row, direction, entity_list):
        """
        Denies access to a node for a given list of entities
        """
        for entity in entity_list:
            self.deny_access(col, row, direction, entity)

    def allow_access_list(self, col, row, direction, entity_list):
        """
        Allows access to a node for a given list of entities
        """
        for entity in entity_list:
            self.allow_access(col, row, direction, entity)

    def deny_home_access(self, entity):
        """
        Denies the entity from accessing the home node
        """
        self.nodes_lookup_table[self.home_key].deny_access(DOWN, entity)

    def allow_home_access(self, entity):
        """
        Allows the entity to access the home node
        """
        self.nodes_lookup_table[self.home_key].allow_access(DOWN, entity)

    def deny_home_access_list(self, entity_list):
        """
        Denies a list of entities from accessing the home node
        """
        for entity in entity_list:
            self.deny_home_access(entity)

    def allow_home_access_list(self, entity_list):
        """
        Allows a list of entities to access the home node
        """
        for entity in entity_list:
            self.allow_home_access(entity)

    def render(self, screen):
        """
        Renders the maze
        """
        for node in self.nodes_lookup_table.values():
            node.render(screen)
