# Modules
from config import config
from screen import screen
import commands
import utils

# Libraries
from llama_cpp import Llama  # type: ignore

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
    response = model(  # type: ignore
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


def start_conversation() -> None:
    n = 0

    while True:
        try:
            prompt = ""

            if n > 0:
                add_spaces()

            prompt = get_prompt()

            if commands.check_command(prompt):
                continue

            response = get_response(prompt)
            respond(get_name(2), response)

            n += 1
        except KeyboardInterrupt:
            if not prompt:
                screen.space()
                screen.exit("Keyboard Interrupt")
            else:
                screen.print("Interrupted 😝")


def get_prompt() -> str:
    name = get_name(1)
    return utils.get_input(f"{name}: ")


def clean_response(text: str) -> str:
    text = re.sub(r"^[^\w]*", "", text)
    text = text.replace("<|im_end|>", "")
    text = text.replace("<|im_start|>assistant", "")
    text = re.sub("\n{2,}", "\n\n", text)

    if config.no_breaks:
        text = text.replace("\n", " ")

    return text.strip()


def get_name(num: int) -> str:
    name = str(getattr(config, f"name_{num}"))

    if not config.nocolors:
        color = getattr(config, f"color_{num}")

        if color:
            name = utils.colortext(color, name)

    avatar = getattr(config, f"avatar_{num}")

    if avatar:
        name = f"{avatar} {name}"

    return name


def respond(name: str, message: str) -> None:
    if not message:
        return

    add_spaces()
    screen.print(f"{name}: {message}")


def add_spaces() -> None:
    if config.compact:
        return

    screen.space()
