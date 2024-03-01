# Modules
from config import config

# Libraries
from prompt_toolkit import prompt, print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.styles import Style


def format_prompt(num: int) -> None:
    avatar = getattr(config, f"avatar_{num}")
    color = getattr(config, f"color_{num}")
    name = getattr(config, f"name_{num}")

    style = Style.from_dict({
        "name": f"ansi{color}"
    })

    if config.avatar_1:
        message = [("class:none", f"{avatar} ")]

    name = f"{name}: "

    if config.no_colors:
        message.append(("class:none", name))
    else:
        message.append(("class:name", name))

    return message, style


def get_input() -> str:
    message, style = format_prompt(1)
    return prompt(message, style=style)


def print_prompt(num: int) -> None:
    message, style = format_prompt(num)
    print_formatted_text(FormattedText(message), style=style, end="")
