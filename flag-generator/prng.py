# Author: Riley Ovenshire
# GitHub username: rileyovenshire
# Date: 1/15/24
# Description: This program generates a random number and writes it to a text file. It is called by the UI.

import random
import time


def read_file(path):
    """monitor prng-service.txt and check to see if the trigger word is included there"""
    with open(path, 'r') as file:
        return file.read().strip()


def write_file(path, content):
    """write the generated number to the prng-service.txt file"""
    with open(path, 'w') as file:
        file.write(str(content))


def main():
    path = 'prng-service.txt'

    while True:
        # check for the trigger word, "run"
        # if it is there, generate the number and write
        if read_file(path) == "run":
            flag_num = random.randint(0, 253)
            write_file(path, flag_num)

        # wait before checking again
        time.sleep(1)


if __name__ == "__main__":
    main()
