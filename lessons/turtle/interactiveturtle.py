import turtle
import random

# -------------------------------------------------------------------------------

# CONFIGURATION
screen = turtle.Screen()

t = turtle.Turtle()

moving_forward = False
moving_backward = False
turning_left = False
turning_right = False

# -------------------------------------------------------------------------------

# START FUNCTIONS
def start_moving_forward():
    global moving_forward
    moving_forward = True

def start_moving_backward():
    global moving_backward
    moving_backward = True

def start_turning_left():
    global turning_left
    turning_left = True

def start_turning_right():
    global turning_right
    turning_right = True

# -------------------------------------------------------------------------------

# STOP FUNCTIONS
def stop_moving_forward():
    global moving_forward
    moving_forward = False

def stop_moving_backward():
    global moving_backward
    moving_backward = False

def stop_turning_left():
    global turning_left
    turning_left = False

def stop_turning_right():
    global turning_right
    turning_right = False

# -------------------------------------------------------------------------------
# FUNCTIONS
    
# DANCE
def dance():
    for _ in range(10):
        t.forward(random.randint(10, 100))
        t.right(random.randint(0, 360))

# CLEAR
def clear_and_reset():
    t.clear()
    t.penup()
    t.home()
    t.pendown()

# MOVE
def move():
    if moving_forward:
        t.forward(10)
    if moving_backward:
        t.backward(10)
    if turning_left:
        t.left(20)
    if turning_right:
        t.right(20)
    screen.ontimer(move, 50)

# -------------------------------------------------------------------------------

# LISTENER
screen.listen()

# -------------------------------------------------------------------------------

# KEYPRESSES
screen.onkeypress(start_moving_forward, "Up")
screen.onkeypress(start_moving_backward, "Down")
screen.onkeypress(start_turning_left, "Left")
screen.onkeypress(start_turning_right, "Right")

screen.onkeyrelease(stop_moving_forward, "Up")
screen.onkeyrelease(stop_moving_backward, "Down")
screen.onkeyrelease(stop_turning_left, "Left")
screen.onkeyrelease(stop_turning_right, "Right")

# RESET and FUNCTIONS
screen.onkey(clear_and_reset, "r")
screen.onkey(dance, "d")
# -------------------------------------------------------------------------------

# LOOPS AND LISTENER
move()
turtle.mainloop()
