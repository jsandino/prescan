import logging
from prescan.batch_loader import BatchLoader
from prescan.deduper import Deduper
from prescan.prescription_classifier import PrescriptionClassifier


class Scanner:
    """
    Orchestrates the processing of all documents in the supplied input directory.
    """

    @staticmethod
    def process_documents(input_dir: str, output_dir: str):
        logger = logging.getLogger(__name__)
        try:
            logger.info("Starting")
            loader = BatchLoader(input_dir, output_dir)

            deduper = Deduper(loader.batches)
            uniques = deduper.get_unique_docs()

            classifier = PrescriptionClassifier(uniques)
            classifier.store_files()

        except Exception as e:
            print(e)
