# Modules
from config import config
from screen import screen
import commands
import textprompt

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
        {"role": "system", "content": config.system},
        {
            "role": "user",
            "content": prompt,
        },
    ]

    added_name = False
    token_printed = False
    last_token = " "

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
                textprompt.print_prompt(2)
                added_name = True

            token = delta["content"]

            if token == "\n":
                if not token_printed:
                    continue
            elif token == " ":
                if last_token == " ":
                    continue

            last_token = token

            if not token_printed:
                token = token.lstrip()
                token_printed = True

            screen.println(token)

    if token_printed:
        screen.space()


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
    return textprompt.get_input()


def add_spaces() -> None:
    if config.compact:
        return

    screen.space()
