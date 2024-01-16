# Author: Riley Ovenshire
# GitHub username: rileyovenshire
# Description: A simple little pinball game made with pygame.

import pygame
import random
import math
import time

pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (0, 0, 128)
LIGHT_BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255,255,0)

# Set the width and height of the screen, game caption
screen_height = 600
screen_width = 800
size = (screen_width, screen_height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pynball")

# ball properties
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
ball_speed_x = 5
ball_speed_y = 5

# paddle properties
paddle_width = 100
paddle_height = 20
left_paddle = pygame.Rect(50, screen_height-60, paddle_width, paddle_height)
right_paddle = pygame.Rect(screen_width-150-paddle_width, screen_height-60, paddle_width, paddle_height)
paddle_speed = 10

# game loop
running = True
while running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #ball movement
    ball_x = ball.x
    ball_y = ball.y
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # ball collision with walls
    if ball_x > screen_width - 20 or ball_x < 0:
        ball_speed_x *= -1
    if ball_y > screen_height - 20 or ball_y < 0:
        ball_speed_y *= -1

    # ball collision with paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_y *= -1

    # paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and left_paddle.x > 0:
        left_paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and left_paddle.x < screen_width - paddle_width:
        left_paddle.x += paddle_speed
    if keys[pygame.K_a] and right_paddle.x > 0:
        right_paddle.x -= paddle_speed
    if keys[pygame.K_d] and right_paddle.x < screen_width - paddle_width:
        right_paddle.x += paddle_speed

    # draw
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()


