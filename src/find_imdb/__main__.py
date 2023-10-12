# Execute with
# $ python -m find_imdb

import os
import sys

if __package__ is None:
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

import main

if __name__ == "__main__":
    usage = ""

    # TODO implement args version to function as module receiving user input
    # args = sys.argv
    # print(args)
    # while len(args) < 2:
    #     print("Invalid parameters")
    # main.main(*args[1:])
