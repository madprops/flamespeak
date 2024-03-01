# Modules
from argparser import ArgParser
from typing import Dict, Any, List

# Standard
import time


class Config:
    # Class to hold all the configuration of the program
    # It also interfaces with ArgParser and processes further

    def __init__(self) -> None:
        self.model = ""
        self.name_1 = "You"
        self.name_2 = "Flame"
        self.avatar_1 = "👽"
        self.avatar_2 = "🔥"
        self.color_1 = "blue"
        self.color_2 = "green"
        self.verbose = False
        self.compact = False
        self.no_breaks = False
        self.no_intro = False
        self.max_tokens = 128
        self.temperature = 0.8
        self.system = ""
        self.log = ""

    class Internal:
        # Time when program started
        start_time = time.time()

        # Argument definitions
        arguments: Dict[str, Any] = {
            "model": {"type": str, "help": "The model to use", "required": True},
            "name-1": {"type": str, "help": "The user's name"},
            "name-2": {"type": str, "help": "The assistant's name"},
            "color-1": {"type": str, "help": "The usercolor"},
            "color-2": {"type": str, "help": "The assistant's name"},
            "avatar-1": {"type": str, "help": "The user's avatar"},
            "avatar-2": {"type": str, "help": "The assistant's avatar"},
            "verbose": {"action": "store_true", "help": "Verbose output"},
            "compact": {"action": "store_true", "help": "Don't add spaces between messages"},
            "no-breaks": {"action": "store_true", "help": "Remove all linebreaks"},
            "no-intro": {"action": "store_true", "help": "Don't show the intro messages"},
            "max-tokens": {"type": int, "help": "Max tokens to use in a single request"},
            "temperature": {"type": float, "help": "The temperature to use in the model"},
            "system": {"type": str, "help": "This tells the model how to act"},
            "log": {"action": "store_true", "help": "Log conversation to this file"},
        }

        aliases: Dict[str, List[str]] = {}

    def parse_args(self) -> None:
        ap = ArgParser("Flamespeak", self.Internal.arguments,
                       self.Internal.aliases, self)

        normals = [
            "model", "name_1", "name_2", "color_1", "color_2",
            "avatar_1", "avatar_2", "verbose", "compact", "no_breaks",
            "no_intro", "max_tokens", "temperature", "system",
        ]

        for normal in normals:
            ap.normal(normal)

        self.check_config()

    def check_config(self) -> None:
        if (not self.system) and (self.name_2):
            self.system = f"You are a guy called {self.name_2}"

        self.color_1 = self.color_1.lower()
        self.color_2 = self.color_2.lower()


config = Config()
