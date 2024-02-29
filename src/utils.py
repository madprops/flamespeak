# Standard
import sys


def dash_to_under(s: str) -> str:
    return s.replace("-", "_")


def under_to_dash(s: str) -> str:
    return s.replace("_", "-")


def msg(message: str) -> None:
    print(message, file=sys.stderr)


def respond(message: str) -> None:
    print(message, file=sys.stdout)


def exit(message: str) -> None:
    msg(f"\nExit: {message}\n")
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


def exit(message: str) -> None:
    msg(f"\nExit: {message}\n")
    sys.exit(1)
