import logging
import shutil
from prescan.batch_loader import BatchLoader
from prescan.deduper import Deduper
from prescan.doc_reader import DocReader


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
            for batch in uniques:
                logger.debug(f"{batch.name}: {len(batch.uniques)} docs")
                for doc in batch.uniques:
                    source = batch.file_path(doc)
                    docReader = DocReader(source)
                    destination = docReader.get_output_file_path(batch.name, doc)
                    shutil.copy(source, destination)

        except Exception as e:
            print(e)
