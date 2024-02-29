# Standard
import re
import sys
import time
from pathlib import Path


def dash_to_under(s: str) -> str:
    return s.replace("-", "_")


def under_to_dash(s: str) -> str:
    return s.replace("_", "-")


def msg(message: str) -> None:
    print(message, file=sys.stderr)


def respond(message: str) -> None:
    print(message, file=sys.stdout)


def get_duration(start: float, end: float) -> str:
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


def resolve_path(path: Path) -> Path:
    pth = Path(path).expanduser()

    if pth.is_absolute():
        return full_path(pth)
    else:
        return full_path(Path(Path.cwd(), pth))


def full_path(path: Path) -> Path:
    return path.expanduser().resolve()


def parse_duration(time_string: str) -> str:
    match = re.match(r"(\d+(\.\d+)?)([smh]+)", time_string)

    if match:
        value, _, unit = match.groups()
        value = float(value)

        if unit == "ms":
            time_string = str(int(value))
        elif unit == "s":
            time_string = str(int(value * 1000))
        elif unit == "m":
            time_string = str(int(value * 60 * 1000))
        elif unit == "h":
            time_string = str(int(value * 60 * 60 * 1000))

    return time_string
