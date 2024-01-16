# Author: Riley Ovenshire
# GitHub username: rileyovenshire
# Date: 1/15/24
# Description: This program reads a text file and finds the flag that is represented by the number in the file, then passes the file path to the UI.

import os
import time


# can conveniently use the exact same code from the prng.py
def read_file(path):
    """monitor image-service.txt and check to see if the trigger word is included there, along with a number"""
    with open(path, 'r') as file:
        return file.read().strip()


def write_file(path, content):
    """write the generated number to the image-service.txt file"""
    with open(path, 'w') as file:
        file.write(str(content))


def main():
    path = 'image-service.txt'
    image_dir = 'C:\\Users\\riley\\projects\\flag-generator\\flag_imgs'
    flag_files = sorted(os.listdir(image_dir))

    while True:
        content = read_file(path)

        if content.endswith(" run"):
            # take just the first element, which is the flag index number that was randomly generated
            index = int(content.split()[0]) % len(flag_files)

            # write the image path to the file
            image_path = os.path.join(image_dir, flag_files[index])
            write_file(path, image_path)

        # check only sporadically
        time.sleep(1)


if __name__ == "__main__":
    main()
