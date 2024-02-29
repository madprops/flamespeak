# Modules
from config import config
import model
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


def main() -> None:
    global last_time
    last_time = config.Internal.start_time

    config.parse_args()
    check_time("Parse Arguments")

    model.prepare_model()
    check_time("Prepare Model")
    utils.msg(utils.colortext("green", "Starting Conversation\n"))

    model.start_conversation()


if __name__ == "__main__":
    main()
