# Modules
from config import config
import utils

# Libraries
from blessed import Terminal

# Standard
import sys
import time


class Screen:
    def __init__(self) -> None:
        self.term = Terminal()

    def print(self, message: str) -> None:
        print(message)

    def println(self, message: str) -> None:
        print(message, end="")

    def clear(self) -> None:
        print(self.term.clear)

    def space(self) -> None:
        self.print("")

    def duration(self) -> None:
        start = config.Internal.start_time
        seconds = int(time.time() - start)
        duration = utils.timestring(seconds)
        self.print(f"Duration: {duration}")

    def exit(self, message: str) -> None:
        self.print(f"\nExit: {message}")
        sys.exit(1)

    def input(self, prompt: str) -> str:
        return input(prompt)


screen = Screen()
