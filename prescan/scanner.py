import logging

from prescan.batch_loader import BatchLoader
from prescan.deduper import Deduper


class Scanner:
    """
    Orchestrates the processing of all documents in the supplied input directory.
    """

    @staticmethod
    def process_documents(input_dir: str):
        logger = logging.getLogger(__name__)
        try:
            logger.info("Starting")
            loader = BatchLoader(input_dir)

            deduper = Deduper(loader.batches)
            uniques = deduper.get_unique_docs()

        except Exception as e:
            print(e)
