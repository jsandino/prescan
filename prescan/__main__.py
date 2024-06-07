import logging
import sys

from prescan.batch_loader import BatchLoader
from prescan.deduper import Deduper
from prescan.doc_reader import DocReader


def main():
    input_dir, log_level = get_input_args()
    logging.basicConfig(
        format="%(levelname)s: %(message)s", encoding="utf-8", level=log_level
    )
    logger = logging.getLogger(__name__)

    try:
        logger.info("Starting")
        loader = BatchLoader(input_dir)

        deduper = Deduper(loader.batches)
        uniques = deduper.get_unique_docs()

    except Exception as e:
        print(e)


def get_input_args() -> tuple[str, int]:
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("Usage: python -m prescan <path_to_docs> [-d]")
        sys.exit(1)

    input_dir = sys.argv[1]
    log_level = (
        logging.DEBUG if len(sys.argv) == 3 and sys.argv[2] == "-d" else logging.INFO
    )

    return input_dir, log_level


if __name__ == "__main__":
    main()