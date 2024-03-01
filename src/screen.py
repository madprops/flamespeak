# Modules
from config import config
import utils

# Libraries
from prompt_toolkit import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import VSplit, HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import WindowAlign, Dimension
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.application import get_app
import pyperclip

# Standard
import sys
import time


class Screen:
    def __init__(self) -> None:
        self.last_prompt = ""
        self.kb = KeyBindings()

        @self.kb.add("c-q")
        def _(event):
            event.app.exit()

        @self.kb.add("c-v")
        def _(event):
            text = pyperclip.paste()

            if text:
                text = text.replace("\n", " ")

            if text:
                event.app.current_buffer.insert_text(text)

        @self.kb.add("enter")
        async def _(event):
            prompt = event.app.current_buffer.text
            self.last_prompt = prompt
            self.clear_input()
            await self.ask_model(prompt)

        @self.kb.add("up")
        def _(event):
            self.set_input(self.last_prompt)

    def print(self, text: str) -> None:
        self.content_buffer.insert_text(f"{text}\n")

    def insert(self, text: str) -> None:
        self.content_buffer.insert_text(text)

    def set_input(self, text) -> None:
        self.input_buffer.text = text
        self.input_buffer.cursor_position = len(self.input_buffer.text)

    def clear_content(self) -> None:
        self.content_buffer.reset()

    def clear_input(self) -> None:
        self.input_buffer.reset()

    def space(self) -> None:
        self.print("\n")

    def duration(self) -> None:
        start = config.Internal.start_time
        seconds = int(time.time() - start)
        duration = utils.timestring(seconds)
        self.print(f"Duration: {duration}")

    def exit(self, message: str) -> None:
        self.print(f"\nExit: {message}")
        sys.exit(1)

    def bottom(self) -> None:
        print(self.term.move(self.term.height, 0))

    def prepare(self) -> None:
        content_buffer = Buffer()
        input_buffer = Buffer(multiline=False)

        layout = Layout(
            HSplit([
                Window(content=BufferControl(buffer=content_buffer), wrap_lines=True),
                Window(height=1, char="-"),
                VSplit([
                    Window(content=FormattedTextControl(FormattedText([("class:prompt", "Input: ")])), dont_extend_width=True),
                    Window(content=BufferControl(buffer=input_buffer), align=WindowAlign.LEFT, width=Dimension(weight=1)),
                ], height=1)
            ])
        )

        layout.focus(input_buffer)
        self.content_buffer = content_buffer
        self.input_buffer = input_buffer
        self.app = Application(key_bindings=self.kb, layout=layout, full_screen=True, mouse_support=True)

    async def run(self) -> None:
        await self.app.run_async()

    def print_prompt(self, num: int, text: str = "") -> None:
        avatar = getattr(config, f"avatar_{num}")
        name = getattr(config, f"name_{num}")
        prompt = f"{avatar} {name}: "
        self.insert(prompt)

        if text:
            self.insert(text)

    async def ask_model(self, prompt: str) -> None:
        from model import stream_response
        await stream_response(prompt)


screen = Screen()
