# Modules
import utils

# Libraries
from blessed import Terminal

# Standard
import sys


class Screen:
    def __init__(self) -> None:
        self.term = Terminal()

    def print(self, message: str) -> None:
        print(message)

    def clear(self) -> None:
        print(self.term.clear)

    def space(self) -> None:
        self.print("")


screen = Screen()
