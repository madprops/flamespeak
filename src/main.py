# Modules
from config import config
from screen import screen
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
    screen.print(f"{label}: {num} seconds")


def check_time(name: str) -> None:
    if config.no_intro:
        return

    global last_time
    now = get_time()
    show_seconds(name, now, last_time)
    last_time = now


def main() -> None:
    # with screen.term.fullscreen():
        global last_time
        last_time = config.Internal.start_time

        config.parse_args()

        model.prepare_model()
        check_time("Prepare Model")

        screen.print(utils.colortext("green", "Starting Conversation"))
        screen.space()

        model.start_conversation()
        screen.exit()


if __name__ == "__main__":
    main()
