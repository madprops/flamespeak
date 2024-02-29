# Modules
from screen import screen
import utils

exit_commands = [
    "quit", "exit", "bye",
    "goodbye", "good bye", "adios",
]

time_commands = [
    "time", "check", "duration",
    "date", "tiempo",
]

clear_commands = [
    "clear", "cls", "clean",
    "wipe", "erase", "reset",
    "empty", "purge", "flush",
]


# Return True to exit the program
def check_command(prompt: str) -> bool:
    if prompt in exit_commands:
        utils.exit("User Exit")
        return True
    elif prompt in time_commands:
        screen.space()
        utils.print_duration()
        return True
    elif prompt in clear_commands:
        screen.clear()
        return True

    return False