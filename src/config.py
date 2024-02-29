# Modules
from argparser import ArgParser
from typing import Dict, Any

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
        self.nocolors = False

    class Internal:
        # Argument definitions
        arguments: Dict[str, Any] = {
            "model": {"type": str, "help": "The model to use", "required": True},
            "name-1": {"type": str, "help": "The user's name"},
            "name-2": {"type": str, "help": "The assistant's name"},
            "color-1": {"type": str, "help": "The usercolor"},
            "color-2": {"type": str, "help": "The assistant's name"},
            "avatar-1": {"type": str, "help": "The user's avatar"},
            "avatar-2": {"type": str, "help": "The assistant's avatar"},
            "nocolors": {"action": "store_true", "help": "Don't use colors"},
            "verbose": {"action": "store_true", "help": "Verbose output"},
        }

        aliases = {}

    def parse_args(self) -> None:
        ap = ArgParser("Flamespeak", self.Internal.arguments, self.Internal.aliases, self)

        ap.normal("model")
        ap.normal("name_1")
        ap.normal("name_2")
        ap.normal("color_1")
        ap.normal("color_2")
        ap.normal("avatar_1")
        ap.normal("avatar_2")
        ap.normal("nocolors")
        ap.normal("verbose")

config = Config()