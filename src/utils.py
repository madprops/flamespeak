# Standard
import sys
import time


def dash_to_under(s: str) -> str:
    return s.replace("-", "_")


def under_to_dash(s: str) -> str:
    return s.replace("_", "-")


def msg(message: str) -> None:
    print(message, file=sys.stderr)


def respond(message: str) -> None:
    print(message, file=sys.stdout)


def get_duration(start: float, end: float) -> float:
    seconds = int(end - start)

    if seconds < 60:
        return f"{seconds} second{'s' if seconds > 1 else ''}"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''}"
    else:
        hours = seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''}"


def exit(message: str) -> None:
    from config import config

    duration = get_duration(config.Internal.start_time, time.time())

    msg(f"\nExit: {message}")
    msg(f"Duration: {duration}\n")

    sys.exit(1)


def colortext(color: str, text: str) -> str:
    codes = {
        "red": "\x1b[31m",
        "green": "\x1b[32m",
        "yellow": "\x1b[33m",
        "blue": "\x1b[34m",
        "magenta": "\x1b[35m",
        "cyan": "\x1b[36m",
    }

    if color in codes:
        code = codes[color]
        text = f"{code}{text}\x1b[0m"

    return text
