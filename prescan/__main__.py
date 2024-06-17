import logging
import sys
from prescan.scanner import Scanner


def main():
    input_dir, output_dir, log_level = get_input_args()
    logging.basicConfig(
        format="%(levelname)s: %(message)s", encoding="utf-8", level=log_level
    )
    Scanner.process_documents(input_dir, output_dir)


def get_input_args() -> tuple[str, int]:
    args = len(sys.argv)
    if args < 2 or args > 4:
        print("Usage: python -m prescan <path_to_docs> <output_dir> [-d]")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = (
        "outputs" if args == 2 or args > 2 and sys.argv[2] == "-d" else sys.argv[2]
    )
    log_level = logging.DEBUG if args == 4 and sys.argv[3] == "-d" else logging.INFO

    return input_dir, output_dir, log_level


if __name__ == "__main__":
    main()
