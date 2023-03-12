"""
Author: Cylix Lee (cylix.lee@foxmail.com).
Created on: March 10th, 2023

A module containing utilities to code easily.
"""
import sys


def fatal(error: str):
    print("Error: {}.".format(error), file=sys.stderr)
    sys.exit()


class UnimplementedException(Exception):
    def __init__(self):
        super().__init__("This functionality is yet to implement.")
