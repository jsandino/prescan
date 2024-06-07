import logging
from prescan.document_batch import DocumentBatch


class Deduper:
    """
    Parses a set of document batches, removing any duplicate documents across different batches
    """

    def __init__(self, batches: list[DocumentBatch]):
        self.batches = batches
        self.logger = logging.getLogger(__name__)

    def get_unique_docs(self) -> list[DocumentBatch]:
        unique_docs = []
        processed_batches = []
        for batch in self.batches:
            self.logger.info(f"==========================")
            self.logger.info(f"Processing batch: {batch.name}")
            self.logger.info(f"==========================")
            filtered_batch = batch.filter_all_duplicates_in(processed_batches)
            unique_docs.append(filtered_batch)
            self.logger.info(filtered_batch.counts())
            self.logger.info("")
            processed_batches.append(batch)

        return unique_docs
