# Modules
from config import config
from screen import screen

# Libraries
from llama_cpp import Llama  # type: ignore

# Standard
import asyncio
import time


class Model:
    def __init__(self) -> None:
        self.mode = None
        self.stream_date = 0

    def prepare(self) -> None:
        self.model = Llama(
            model_path=str(config.model),
            verbose=config.verbose,
        )

    async def stream(self, prompt: str) -> None:
        prompt = prompt.strip()

        if not prompt:
            return

        self.space()
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
        date = time.time()
        self.stream_date = date

        output = self.model.create_chat_completion(  # type: ignore
            messages=messages,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            stream=True,
        )

        for chunk in output:
            if date != self.stream_date:
                break

            delta = chunk["choices"][0]["delta"]

            if "content" in delta:
                if not added_name:
                    self.space()
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

    def space(self) -> None:
        if config.compact:
            return

        screen.space()


model = Model()
