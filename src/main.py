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


def get_seconds(name: str, start: float, end: float) -> str:
    num = round(start - end, 3)
    return (f"{name}: {num} seconds")


def check_time(name: str) -> str:
    if config.no_intro:
        return

    global last_time
    now = get_time()
    seconds = get_seconds(name, now, last_time)
    last_time = now
    return seconds


async def main() -> None:
    global last_time
    last_time = config.Internal.start_time
    config.parse_args()

    if not model.load():
        return

    duration = check_time("Loading Complete")
    screen.prepare(duration)
    await screen.run()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
