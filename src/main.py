# Modules
from config import config
import assistant
import utils

# Standard
import time

# Performance
last_time = 0.0


def get_time() -> float:
    return time.time()


def show_seconds(name: str, start: float, end: float) -> None:
    num = round(start - end, 3)
    label = utils.colortext("blue", name)
    utils.msg(f"{label}: {num} seconds")


def check_time(name: str) -> None:
    if config.no_intro:
        return

    global last_time
    now = get_time()
    show_seconds(name, now, last_time)
    last_time = now


def main():
    global last_time
    start_time = get_time()
    last_time = start_time

    config.parse_args()
    check_time("Parse Args")

    assistant.prepare_assistant()
    check_time("Prepare Assistant")
    utils.msg("Starting Conversation...\n")

    assistant.start_conversation()


if __name__ == "__main__":
    main()
