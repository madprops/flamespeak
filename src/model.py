# Modules
from config import config
from screen import screen

# Libraries
from llama_cpp import Llama  # type: ignore

# Standard
import asyncio

model = None


def prepare_model() -> None:
    global model

    model = Llama(
        model_path=config.model,
        verbose=config.verbose,
    )


async def stream_response(prompt: str) -> None:
    prompt = prompt.strip()

    if not prompt:
        return

    add_space()
    screen.print_prompt(1, prompt)

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
                add_space()
                screen.print_prompt(2)
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

            screen.insert(token)

        await asyncio.sleep(0.1)

    if token_printed:
        screen.space()


def add_space() -> None:
    if config.compact:
        return

    screen.space()
