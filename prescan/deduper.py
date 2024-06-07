import filecmp
import logging
import os
from prescan.document_batch import DocumentBatch
from collections import defaultdict


class Deduper:
    """
    Parses a set of document batches, removing any duplicate documents across different batches
    """

    def __init__(self, batches: list[DocumentBatch]):
        self.batches = batches
        self.logger = logging.getLogger(__name__)

    def get_unique_docs(self) -> dict[str : set[str]]:
        unique_docs = {}
        processed_batches = []
        for batch in self.batches:
            self.logger.info(f"==========================")
            self.logger.info(f"Processing batch: {batch.name}")
            self.logger.info(f"==========================")
            batch.filter_all_duplicates_in(processed_batches)
            processed_batches.append(batch)
            unique_docs[batch.name] = batch.uniques
            self.logger.info(batch.counts())
            self.logger.info("")

        return unique_docs
