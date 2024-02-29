# Modules
from config import config
import utils

# Libraries
from llama_cpp import Llama

# Standard
import re

assistant = None


def prepare_assistant() -> None:
    global assistant

    assistant = Llama(
        model_path=config.model,
        verbose=config.verbose,
    )


def get_response(prompt: str) -> str:
    response = assistant(prompt)
    choices = response.get("choices")
    text = ""

    if choices:
        text = choices[0].get("text", "").strip()
        text = clean_response(text)

    return text


def check_command(prompt: str) -> bool:
    cmd = prompt.lower()

    if not cmd.startswith("/"):
        return False

    cmd = cmd[1:]

    if cmd in ["quit", "exit"]:
        utils.exit("User Exit")

    return True


def start_conversation() -> None:
    while True:
        try:
            prompt = get_prompt()

            if check_command(prompt):
                continue

            response = get_response(prompt)

            if response:
                name = get_name(2)
                utils.respond(f"{name}: {response}")
        except KeyboardInterrupt:
            utils.exit("Keyboard Interrupt")


def get_prompt() -> str:
    name = get_name(1)
    return input(f"{name}: ")


def clean_response(text: str) -> str:
    pattern = re.compile(r"^(?P<noise>[ .,;\\n]*)(\w+)")
    match = re.match(pattern, text)

    if match:
        return text.lstrip(match.group("noise"))
    else:
        return text


def get_name(num: int) -> str:
    name = getattr(config, f"name_{num}")

    if not config.nocolors:
        color = getattr(config, f"color_{num}")

        if color:
            name = utils.colortext(color, name)

    avatar = getattr(config, f"avatar_{num}")

    if avatar:
        name = f"{avatar} {name}"

    return name
