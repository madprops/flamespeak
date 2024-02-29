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


def stream_response(prompt: str):
    messages = [
        {"role": "system", "content": f"You are a guy called {config.name_2}"},
        {
            "role": "user",
            "content": prompt,
        },
    ]

    added_name = False
    token_printed = False
    last_token = ""

    output = model.create_chat_completion(  # type: ignore
        messages=messages,
        max_tokens=config.max_tokens,
        temperature=config.temperature,
        stream=True,
    )


    for chunk in output:
        delta = chunk["choices"][0]["delta"]

        if "content" in delta:
            if not added_name:
                add_spaces()
                name = get_name(2)
                screen.println(f"{name}: ")
                added_name = True

            token = delta["content"]
            token = re.sub(r"\<\|im_start\|\>assistant", f"{get_name(2)}: ", token, re.IGNORECASE)
            token = re.sub(r"\<\|im_end\|\>", "\n", token, re.IGNORECASE)
            token = re.sub(r"\<\|im_end\|\>", "\n", token, re.IGNORECASE)

            if token == "\n":
                if not token_printed:
                    continue
            elif token == " ":
                if last_token == " ":
                    continue

            last_token = token
            token_printed = True
            screen.println(token)


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

            stream_response(prompt)

            n += 1
        except KeyboardInterrupt:
            if not prompt:
                screen.space()
                screen.exit("Keyboard Interrupt")
            else:
                screen.print("Interrupted 😝")


def get_prompt() -> str:
    name = get_name(1)
    return screen.input(f"{name}: ")


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


def add_spaces() -> None:
    if config.compact:
        return

    screen.space()
