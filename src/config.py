# Modules
from argparser import ArgParser
from typing import Dict, Any, List, Union

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
            "max-tokens": {"type": int, "help": "Max tokens to use in a single request"},
            "temperature": {"type": float, "help": "The temperature to use in the model"},
            "system": {"type": str, "help": "This tells the model how to act"},
            "log": {"type": str, "help": "Log conversation to this file"},
        }

        normals = [
            "name_1", "name_2", "color_1", "color_2",
            "avatar_1", "avatar_2", "verbose", "compact", "no_breaks",
        ]

        paths = ["model", "log"]
        aliases: Dict[str, List[str]] = {}
        ap: Union[ArgParser, None] = None

    def parse_args(self) -> None:
        self.Internal.ap = ArgParser("Flamespeak", self.Internal.arguments,
                                     self.Internal.aliases, self)

        assert isinstance(self.Internal.ap, ArgParser)

        for normal in self.Internal.normals:
            self.Internal.ap.normal(normal)

        for path in self.Internal.paths:
            self.Internal.ap.path(path)

        self.check_config()

    def check_config(self) -> None:
        if (not self.system) and (self.name_2):
            self.system = f"You are a guy called {self.name_2}"

        self.color_1 = self.color_1.lower()
        self.color_2 = self.color_2.lower()

    def get_argument(self, name: str) -> Union[Dict[str, Any], None]:
        name = ArgParser.under_to_dash(name)
        return self.Internal.arguments.get(name)


config = Config()
