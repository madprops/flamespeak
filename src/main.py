# Modules
from config import config
import assistant


def main():
    config.parse_args()
    assistant.prepare_assistant()
    assistant.start_conversation()


if __name__ == "__main__":
    main()
