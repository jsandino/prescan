import logging
import shutil
from prescan.doc_reader import DocReader
from prescan.document_batch import DocumentBatch


class PrescriptionClassifier:
    """
    Stores documents in two different locations, based on whether the document corresponds to a prescription.
    """

    def __init__(self, batches: list[DocumentBatch]):
        logger = logging.getLogger(__name__)
        self.batches = batches

    def store_files(self):
        for batch in self.batches:
            self.logger.debug(f"{batch.name}: {len(batch.uniques)} docs")
            for doc in batch.uniques:
                source = batch.file_path(doc)
                docReader = DocReader(source, batch.output_dir_path)
                destination = docReader.get_output_file_path(batch.name, doc)
                shutil.copy(source, destination)
