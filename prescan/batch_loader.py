import logging
import os
from prescan.document_batch import DocumentBatch


class BatchLoader:
    """
    Scans an input directory and loads all document batches under it
    """

    _batch_prefix = "faxes"

    def __init__(self, input_dir, output_dir):
        self.logger = logging.getLogger(__name__)
        BatchLoader._validate(input_dir)
        self._batches = BatchLoader._load_batches(input_dir, output_dir)
        self.logger.debug(f"Batches loaded: {self._batches}")

    @property
    def batches(self):
        return self._batches

    @classmethod
    def _validate(cls, path):
        if not os.path.exists(path):
            raise Exception("Specified input directory is missing")

    @classmethod
    def _load_batches(cls, input_dir: str, output_dir: str) -> list[DocumentBatch]:
        """
        Loads all fax batches in chronological order.
        """
        return [
            DocumentBatch(name, input_path, output_path)
            for name, input_path, output_path in BatchLoader._load_all(
                input_dir, output_dir
            )
        ]

    @classmethod
    def _load_all(cls, input_dir: str, output_dir: str) -> list[(str, str, str)]:
        """
        Loads all input directories matching the batch prefix ("faxes"), keeping the
        chronological order as specified by the integer suffix in the directory name
        (ie faxes-1 arrived before faxes-2).
        """
        dirs = []
        for name in os.listdir(input_dir):
            input_path = os.path.join(input_dir, name)
            output_path = os.path.join(output_dir, name)
            if BatchLoader.is_batch_dir(input_path, name):
                dirs.append((name, input_path, output_path))

        return sorted(dirs, key=lambda dir: dir[0])  # sort by subdirectory name

    @classmethod
    def is_batch_dir(cls, path, name):
        return os.path.isdir(path) and name.startswith(BatchLoader._batch_prefix)
