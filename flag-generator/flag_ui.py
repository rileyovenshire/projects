# Author: Riley Ovenshire
# GitHub username: rileyovenshire
# Date: 1/15/24
# Description: This program gives a user a clickable button that triggers the generation of a random number.
#   Then, the program waits for a file path to be returned. Once the file path is returned, the program reads the file
#   and displays the flag that is represented by that number.

import tkinter as tk
from PIL import Image, ImageTk
import os
import time


def read_file(path):
    """reads file"""
    with open(path, 'r') as file:
        return file.read().strip()


def write_file(path, content):
    """writes to file"""
    with open(path, 'w') as file:
        file.write(str(content))


def display_flag():
    """actual UI driver code, this is what will call the prng and image locating services"""

    # once called, write run to prng
    write_file('prng-service.txt', 'run')

    # wait for response
    while True:
        prng_num = read_file("prng-service.txt")
        if prng_num.isdigit():
            break
        time.sleep(1)

    # write the number to the image service
    write_file('image-service.txt', prng_num + ' run')

    # wait for response
    while True:
        img_path = read_file("image-service.txt")
        if os.path.isfile(img_path):
            break
        time.sleep(1)

    # pass the image to the UI
    load_img = Image.open(img_path)
    load_img = load_img.resize((300, 200), Image.ANTIALIAS)
    render_img = ImageTk.PhotoImage(load_img)
    img_label.config(image=render_img)
    img_label.image = render_img

# init tkinter
root = tk.Tk()
root.title("Vexillology")
label = tk.Label(root, text="Click the button to show a flag.")
label.pack()

show_flag_button = tk.Button(root, text="Show Flag", command=display_flag)
show_flag_button.pack()

img_label = tk.Label(root)
img_label.pack()

root.mainloop()