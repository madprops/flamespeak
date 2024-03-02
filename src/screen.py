# Modules
from config import config
import utils

# Libraries
from prompt_toolkit import Application  # type: ignore
from prompt_toolkit.buffer import Buffer  # type: ignore
from prompt_toolkit.layout.containers import VSplit, HSplit, Window  # type: ignore
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl  # type: ignore
from prompt_toolkit.formatted_text import FormattedText  # type: ignore
from prompt_toolkit.layout.layout import Layout  # type: ignore
from prompt_toolkit.key_binding import KeyBindings  # type: ignore
from prompt_toolkit.layout import WindowAlign, Dimension  # type: ignore
from prompt_toolkit.key_binding.key_processor import KeyPressEvent  # type: ignore
from prompt_toolkit.buffer import Buffer
import pyperclip  # type: ignore

# Standard
import time


class Screen:
    def __init__(self) -> None:
        self.last_prompt = ""
        self.kb = KeyBindings()

        @self.kb.add("c-q")  # type: ignore
        def _(event: KeyPressEvent) -> None:
            event.app.exit()

        @self.kb.add("c-v")  # type: ignore
        def _(event: KeyPressEvent) -> None:
            text = pyperclip.paste()

            if text:
                text = text.replace("\n", " ")

            if text:
                event.app.current_buffer.insert_text(text)

        @self.kb.add("enter")  # type: ignore
        async def _(event: KeyPressEvent) -> None:
            await self.on_enter()

        @self.kb.add("up")  # type: ignore
        def _(event: KeyPressEvent) -> None:
            self.set(self.input_buffer, self.last_prompt)

        @self.kb.add("escape")  # type: ignore
        def _(event: KeyPressEvent) -> None:
            self.clear_input()

    def print(self, text: str) -> None:
        self.content_buffer.insert_text(f"{text}\n")

    def insert(self, text: str) -> None:
        self.cursor_to_end(self.content_buffer)
        self.content_buffer.insert_text(text)

    def set(self, buffer: Buffer, text: str) -> None:
        buffer.text = text
        self.cursor_to_end(buffer)

    def cursor_to_start(self, buffer: Buffer) -> None:
        buffer.cursor_position = 0

    def cursor_to_end(self, buffer: Buffer) -> None:
        buffer.cursor_position = len(buffer.text)

    def clear_content(self) -> None:
        self.clear_buffer(self.content_buffer)

    def clear_input(self) -> None:
        self.clear_buffer(self.input_buffer)

    def space(self) -> None:
        self.print("\n")

    def clear_buffer(self, buffer: Buffer) -> None:
        buffer.text = ""

    def duration(self) -> None:
        start = config.Internal.start_time
        seconds = int(time.time() - start)
        duration = utils.timestring(seconds)
        self.print(f"Duration: {duration}")

    def exit(self) -> None:
        self.app.exit()

    def prepare(self, duration) -> None:
        content_buffer = Buffer()
        content_buffer.text = ""
        content_buffer.insert_text(duration + "\n")
        content_buffer.insert_text(f"Model: {config.model}\n")
        content_buffer.insert_text(f"Name 1: {config.name_1}\n")
        content_buffer.insert_text(f"Name 2: {config.name_2}")
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
        from model import model
        await model.stream(prompt)

    async def on_enter(self) -> None:
        from commands import check_command
        prompt = self.input_buffer.text
        self.last_prompt = prompt
        self.clear_input()

        if check_command(prompt):
            return

        await self.ask_model(prompt)


screen = Screen()
