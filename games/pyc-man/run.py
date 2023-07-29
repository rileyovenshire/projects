# Configuration file to run the application

import pygame
from pygame.locals import *
from constants import *
from sprites import LifeSprites
from sprites import FruitSprites
from pellets import PelletGroup
from text import TextGroup
from vector import Vector2
from pycman import Pycman
from ghosts import GhostGroup
from pause import Pause
from sprites import MazeSprites
from mazedata import MazeData
from nodes import NodeGroup
from fruit import Fruit


class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.background_normal = None
        self.background_flash = None
        self.clock = pygame.time.Clock()
        self.fruit = None
        self.pause = Pause(True)
        self.level = 1
        self.lives = 3
        self.score = 0
        self.textgroup = TextGroup()
        self.life_sprites = LifeSprites(self.lives)
        self.flash_bg = False
        self.flash_time = 0.2
        self.flash_timer = 0
        self.fruit_eaten = []
        self.fruit_nodes = None
        self.maze_data = MazeData()

    def set_background(self):
        """
        Set the background of the game
        """
        self.background_normal = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_normal.fill(BLACK)
        self.background_flash = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_flash.fill(BLACK)
        self.background_normal = self.mazesprites.construct_background(self.background_normal, self.level % 5)
        self.background_flash = self.mazesprites.construct_background(self.background_flash, 5)
        self.flash_bg = False
        self.background = self.background_normal

    def start_game(self):
        """
        Creates instance of the game.
        """
        self.maze_data.load_maze(self.level)
        self.mazesprites = MazeSprites(self.maze_data.obj.name + ".txt", self.maze_data.obj.name + "_rotation.txt")
        self.set_background()
        self.nodes = NodeGroup(self.maze_data.obj.name + ".txt")
        self.maze_data.obj.set_portal_pairs(self.nodes)
        self.maze_data.obj.connect_home_nodes(self.nodes)
        self.pycman = Pycman(self.nodes.get_node_from_grid(*self.maze_data.obj.pycman_start))
        self.pellets = PelletGroup(self.maze_data.obj.name + ".txt")
        self.ghosts = GhostGroup(self.nodes.get_start_temp_node(), self.pycman)

        self.ghosts.pinky.set_start_node(self.nodes.get_node_from_grid(*self.maze_data.obj.add_offset(2, 3)))
        self.ghosts.inky.set_start_node(self.nodes.get_node_from_grid(*self.maze_data.obj.add_offset(0, 3)))
        self.ghosts.clyde.set_start_node(self.nodes.get_node_from_grid(*self.maze_data.obj.add_offset(4, 3)))
        self.ghosts.blinky.set_start_node(self.nodes.get_node_from_grid(*self.maze_data.obj.add_offset(2, 0)))
        self.ghosts.set_spawn_node(self.nodes.get_node_from_grid(*self.maze_data.obj.add_offset(2, 3)))

        self.nodes.deny_home_access(self.pycman)
        self.nodes.deny_home_access_list(self.ghosts)
        self.ghosts.inky.start_node.deny_access(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.start_node.deny_access(LEFT, self.ghosts.clyde)
        self.maze_data.obj.deny_ghosts_access(self.ghosts, self.nodes)

    def update(self):
        """
        Update the game
        """
        dt = self.clock.tick(30) / 1000.0
        self.textgroup.update(dt)
        self.pellets.update(dt)
        if not self.pause.paused:
            self.ghosts.update(dt)
            if self.fruit is not None:
                self.fruit.update(dt)
            self.check_pellet_events()
            self.check_ghost_events()
            self.check_fruit_events()

        if self.pycman.alive:
            if not self.pause.paused:
                self.pycman.update(dt)
        else:
            self.pycman.update(dt)

        if self.flash_bg:
            self.flash_timer += dt
            if self.flash_timer >= self.flash_time:
                self.flash_timer = 0
                if self.background == self.background_normal:
                    self.background = self.background_flash
                else:
                    self.background = self.background_normal

        after_pause = self.pause.update(dt)
        if after_pause is not None:
            after_pause()
        self.check_events()
        self.render()


    def check_events(self):
        """
        Check for events
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pycman.alive:
                        self.pause.set_pause(player_paused=True)
                        if not self.pause.paused:
                            self.textgroup.hide_text()
                            self.show_entities()
                        else:
                            self.textgroup.show_text(PAUSETXT)

    def check_pellet_events(self):
        """
        Check for pellet events
        """
        pellet = self.pycman.eat_pellets(self.pellets.pellet_list)
        if pellet:
            self.pellets.num_eaten += 1
            self.update_score(pellet.points)
            if self.pellets.num_eaten == 30:
                self.ghosts.inky.start_node.allow_access(RIGHT, self.ghosts.inky)
            elif self.pellets.num_eaten == 70:
                self.ghosts.clyde.start_node.allow_access(LEFT, self.ghosts.clyde)
            self.pellets.pellet_list.remove(pellet)
            if pellet.name == POWERPELLET:
                self.ghosts.start_fright()
            if self.pellets.is_empty():
                self.flash_bg = True
                self.hide_entities()
                self.pause.set_pause(pause_time=3, func=self.next_level)

    def check_ghost_events(self):
        """
        Check for ghost events
        """
        for ghost in self.ghosts:
            if self.pycman.collide_ghost(ghost):
                if ghost.mode.current is FRIGHT:
                    self.pycman.visible = False
                    ghost.visible = False
                    self.update_score(ghost.points)
                    self.textgroup.add_text(str(ghost.points), WHITE, ghost.position.x, ghost.position.y, 8, time=1)
                    self.ghosts.update_points()
                    self.pause.set_pause(pause_time=1, func=self.show_entities)
                    ghost.start_spawn()
                    self.nodes.allow_home_access(ghost)
                elif ghost.mode.current is not SPAWN:
                    if self.pycman.alive:
                        self.lives -= 1
                        self.life_sprites.remove_image()
                        self.pycman.die()
                        self.ghosts.hide()
                        if self.lives <= 0:
                            self.textgroup.show_text(GAMEOVERTXT)
                            self.pause.set_pause(pause_time=3, func=self.restart_game)
                        else:
                            self.pause.set_pause(pause_time=3, func=self.reset_level)

    def check_fruit_events(self):
        """
        Check for fruit events
        """
        if self.pellets.num_eaten == 50 or self.pellets.num_eaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.get_node_from_grid(9, 20), self.level)
                print(self.fruit)
            if self.fruit is not None:
                if self.pycman.collision(self.fruit):
                    self.update_score(self.fruit.points)
                    self.textgroup.add_text(str(self.fruit.points), WHITE, self.fruit.position.x, self.fruit.position.y,
                                            8, time=1)
                    fruit_eaten = False
                    for fruit in self.fruit_eaten:
                        if fruit.get_offset() == self.fruit.image.get_offset():
                            self.fruit_eaten = True
                            break
                        if not fruit_eaten:
                            self.fruit_eaten.append(self.fruit.image)
                    self.fruit = None
                elif self.fruit.destroy:
                    self.fruit = None

    def show_entities(self):
        """
        Show the entities
        """
        self.pycman.visible = True
        self.ghosts.show()

    def hide_entities(self):
        """
        Hide the entities
        """
        self.pycman.visible = False
        self.ghosts.hide()

    def next_level(self):
        """
        Advances to the next level
        """
        self.show_entities()
        self.level += 1
        self.pause.paused = True
        self.start_game()
        self.textgroup.update_level(self.level)

    def restart_game(self):
        self.lives = 3
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.start_game()
        self.score = 0
        self.textgroup.update_score(self.score)
        self.textgroup.update_level(self.level)
        self.textgroup.show_text(READYTXT)
        self.life_sprites.reset_lives(self.lives)
        self.fruit_eaten = []

    def reset_level(self):
        """
        Resets the current level
        """
        self.pause.paused = True
        self.pycman.reset()
        self.ghosts.reset()
        self.fruit = None
        self.textgroup.show_text(READYTXT)

    def update_score(self, points):
        """
        Updates the score
        """
        self.score += points
        self.textgroup.update_score(self.score)

    def render(self):
        """
        Render the game
        """
        self.screen.blit(self.background, (0, 0))
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pycman.render(self.screen)
        self.ghosts.render(self.screen)
        self.textgroup.render(self.screen)

        for i in range(len(self.life_sprites.images)):
            x = self.life_sprites.images[i].get_width() * i
            y = SCREENHEIGHT - self.life_sprites.images[i].get_height()
            self.screen.blit(self.life_sprites.images[i], (x, y))

        for i in range(len(self.fruit_eaten)):
            x = SCREENWIDTH - self.fruit_eaten[i].get_width() * (i + 1)
            y = SCREENHEIGHT - self.fruit_eaten[i].get_height()
            self.screen.blit(self.fruit_eaten[i], (x, y))

        pygame.display.update()


# -------------------------------------------------
if __name__ == "__main__":
    game = GameController()
    game.start_game()
    while True:
        game.update()
