import turtle
import random
import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
import math

# WELCOME TO TURTLEPYLOT!
# Configuration
screen = turtle.Screen()
screen.title("Turtlepylot")
screen.setup(width=800, height=600)
t = turtle.Turtle()
t.speed(1)

screen_width, screen_height = 800 / 2, 600 / 2
normal_speed, boosted_speed = 10, 100
current_speed = normal_speed
moving_forward = moving_backward = turning_left = turning_right = is_drawing = False


# -------------------------------------------------------------------------------
# MOVEMENT FUNCTIONS
# -------------------------------------------------------------------------------

def start_moving_forward():
    global moving_forward
    if is_drawing:
        return
    moving_forward = True

def start_moving_backward():
    global moving_backward
    if is_drawing:
        return
    moving_backward = True

def start_turning_left():
    global turning_left
    turning_left = True

def start_turning_right():
    global turning_right
    turning_right = True

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

def boost_speed():
    """
    Pedal to the metal!

    Hold the spacebar to activate.
    """
    global current_speed
    if is_drawing:
        return
    current_speed = boosted_speed

def normalize_speed():
    """
    Slow down there, speed racer.

    Release the spacebar to activate.
    """
    global current_speed
    if is_drawing:
        return
    current_speed = normal_speed

def move():
    """
    Moves automatically depending on keypresses.
    """
    global moving_forward, moving_backward, turning_left, turning_right

    if is_drawing:
        screen.ontimer(move, 50)
        return

    # get current position
    heading = t.heading()
    x, y = t.pos()

    if moving_forward:
        nx = x + current_speed * math.cos(math.radians(heading))
        ny = y + current_speed * math.sin(math.radians(heading))
        if -screen_width / 2 < nx < screen_width / 2 and -screen_height / 2 < ny < screen_height / 2:
            t.goto(nx, ny)
        else:
            t.forward(current_speed)
    if moving_backward:
        nx = x - current_speed * math.cos(math.radians(heading))
        ny = y - current_speed * math.sin(math.radians(heading))
        if -screen_width / 2 < nx < screen_width / 2 and -screen_height / 2 < ny < screen_height / 2:
            t.goto(nx, ny)
        else:
            t.backward(current_speed)
    if turning_left:
        t.left(20)
    if turning_right:
        t.right(20)
    screen.ontimer(move, 50)

# -------------------------------------------------------------------------------
# FEATURE FUNCTIONS
# -------------------------------------------------------------------------------
def dance():
    """
    Fun little function that makes the turtle dance.

    Press 'd' to activate.
    """
    for _ in range(10):
        t.forward(random.randint(10, 100))
        t.right(random.randint(0, 360))

def clear_and_reset():
    """
    Clears the screen and centers the turtle.

    Press 'r' to activate.
    """
    t.clear()
    t.penup()
    t.home()
    t.pendown()

def draw_shape():
    """
    Shape assistant. The user will select a shape from the dropdown GUI, the 
    turtle will draw the shape.
    """
    global is_drawing
    if is_drawing:
        return
    is_drawing = True
    
    shape = shape_combo.get().upper()
    if shape == "CIRCLE":
        t.circle(50)
    elif shape == "SQUARE":
        for _ in range(4):
            t.forward(100)
            t.right(90)
    
    is_drawing = False

def pick_color():
    """
    Opens a color selection dialog and sets the turtle's color to the chosen color.
    """
    color = colorchooser.askcolor(title="Pick a color")[1]
    if color:
        t.pencolor(color)

def thick_pen(event):
    """
    Increases the thickness of the pen.
    """
    thickness = int(thickness_scale.get())
    t.pensize(thickness)

# -------------------------------------------------------------------------------
# KEYBINDINGS AND FUCTIONALITY
# -------------------------------------------------------------------------------
def setup_keybindings():
    '''
    Keybindings for movement and functions.

    Movement keys: Up, Down, Left, Right
    Reset: r
    Dance: d
    Boost: Space (hold)
    '''
    screen.listen()

    # Movement
    screen.onkeypress(start_moving_forward, "Up")
    screen.onkeypress(start_moving_backward, "Down")
    screen.onkeypress(start_turning_left, "Left")
    screen.onkeypress(start_turning_right, "Right")

    screen.onkeyrelease(stop_moving_forward, "Up")
    screen.onkeyrelease(stop_moving_backward, "Down")
    screen.onkeyrelease(stop_turning_left, "Left")
    screen.onkeyrelease(stop_turning_right, "Right")

    # Functions
    screen.onkey(clear_and_reset, "r")
    screen.onkey(dance, "d")
    screen.onkeypress(boost_speed, "space")
    screen.onkeyrelease(normalize_speed, "space")


# -------------------------------------------------------------------------------
# GUI
# -------------------------------------------------------------------------------
def setup_gui():
    '''
    GUI configurations. Contains shape drawing, color picking, and pen thickness.
    '''
    global shape_combo, thickness_scale
    root = tk.Tk()
    root.title("Drawing Menu")

    shapedrawing = tk.Label(root, text="Shape Drawing")
    shapedrawing.pack(pady=5)

    shape_combo = ttk.Combobox(root, values=["Circle", "Square"])
    shape_combo.pack(pady=5)

    draw_button = ttk.Button(root, text="Draw", command=draw_shape)
    draw_button.pack(pady=5)

    color_button = ttk.Button(root, text="Pick Color", command=pick_color)
    color_button.pack(pady=5)

    thickness_label = tk.Label(root, text="Pen Thickness")
    thickness_label.pack(pady=(10, 5))

    thickness_scale = tk.Scale(root, from_=1, to=20, orient='horizontal', command=thick_pen)
    thickness_scale.pack(pady=5)
    thickness_scale.set(1)

    root.geometry("200x300")
    root.update()
    root.deiconify()

# -------------------------------------------------------------------------------
# MAINLOOP
# -------------------------------------------------------------------------------
if __name__ == "__main__":
    setup_gui()
    setup_keybindings()
    move()
    turtle.mainloop()