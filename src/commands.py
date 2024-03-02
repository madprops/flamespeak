# Modules
from screen import screen
from config import config

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
        screen.exit()
        return True
    elif prompt in time_commands:
        screen.duration()
        return True
    elif prompt in clear_commands:
        screen.clear_content()
        return True
    elif "=" in prompt:
        return change_config(prompt)

    return False


def change_config(text: str) -> bool:
    words = text.split("=")
    words = list(filter(None, map(str.strip, words)))

    if (len(words) >= 2):
        config_name = words[0]
        config_value = " ".join(words[1:])

        def convert(vtype, value):
            return vtype(value)

        if config_name in config.Internal.normals:
            try:
                arg = config.get_argument(config_name)

                if arg:
                    value = convert(arg["type"], config_value)
                    config.Internal.ap.normal(config_name, value)
            except BaseException:
                return False
        elif config_name in config.Internal.paths:
            try:
                config.Internal.ap.path(config_name, config_value)
            except BaseException:
                return False
        else:
            return False

        screen.print(f"* {config_name} set to {config_value} *")
        return True

    return False
