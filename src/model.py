# Modules
from config import config
import utils

# Libraries
from llama_cpp import Llama

# Standard
import re

model = None


def prepare_model() -> None:
    global model

    model = Llama(
        model_path=config.model,
        verbose=config.verbose,
    )


def get_response(prompt: str) -> str:
    response = model(
        prompt=prompt,
        max_tokens=config.max_tokens,
        temperature=config.temperature,
    )

    choices = response.get("choices")
    text = ""

    if choices:
        text = choices[0].get("text", "")
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
    n = 0

    while True:
        try:
            if n > 0:
                add_spaces()

            prompt = get_prompt()

            if check_command(prompt):
                continue

            response = get_response(prompt)

            if response:
                add_spaces()
                respond(get_name(2), response)

            n += 1
        except KeyboardInterrupt:
            utils.exit("Keyboard Interrupt")


def get_prompt() -> str:
    name = get_name(1)
    return input(f"{name}: ")


def clean_response(text: str) -> str:
    pattern = re.compile(r"^(?P<noise>[ .,;\\n]*)(\w+)")
    match = re.match(pattern, text)

    if match:
        text = text.lstrip(match.group("noise"))

    if config.no_breaks:
        text = text.replace("\n", " ")

    return text.strip()


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


def respond(name: str, message: str) -> None:
    utils.respond(f"{name}: {message}")


def add_spaces():
    if config.spacing <= 0:
        return

    for _ in range(config.spacing):
        utils.respond("")
