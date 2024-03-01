# Modules
from config import config
from screen import screen
from model import model
import utils

# Standard
import time
import asyncio

# Performance
last_time = 0.0


def get_time() -> float:
    return time.time()


def show_seconds(name: str, start: float, end: float) -> None:
    num = round(start - end, 3)
    label = utils.colortext("blue", name)
    screen.print(f"{label}: {num} seconds")


def check_time(name: str) -> None:
    if config.no_intro:
        return

    global last_time
    now = get_time()
    show_seconds(name, now, last_time)
    last_time = now


async def main() -> None:
    global last_time
    last_time = config.Internal.start_time
    config.parse_args()
    model.prepare()
    screen.prepare()
    await screen.run()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
