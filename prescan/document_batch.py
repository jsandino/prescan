import copy
import filecmp
import logging
import os


class DocumentBatch:
    """
    Representation of a set of documents e-faxed in a bundle.
    """

    def __init__(self, name, docpath):
        self.logger = logging.getLogger(__name__)
        self.name = name
        self.path = docpath
        self.faxes = set(os.listdir(docpath))
        self.uniques = set(self.faxes)

    def copy(self):
        return copy.copy(self)

    def file_path(self, file_name):
        return os.path.join(self.path, file_name)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.name}: {len(self.faxes)} docs"

    def __len__(self):
        return len(self.faxes)

    def filter_all_duplicates_in(
        self, batches: list["DocumentBatch"]
    ) -> "DocumentBatch":
        """
        Filters out documents in this batch that are also present in any of the supplied input batches.
        The resulting DocumentBatch is a copy of this batch minus the duplicate documents.
        """

        new_batch = self.copy()

        if not batches:
            new_batch.uniques.update(new_batch.faxes)

        for batch in batches:
            new_docs = new_batch.filter_duplicates_present_in(batch)
            new_batch.uniques = new_docs

        return new_batch

    def filter_duplicates_present_in(self, batch: "DocumentBatch"):
        """
        Filters out documents in this batch that are also present in the supplied batch.
        """
        new_docs = self.uniques
        existing_docs = batch.faxes

        potential_dups = new_docs & existing_docs
        self.logger.debug(
            f"Potential duplicates from {batch.name}: {len(potential_dups)}"
        )

        dups = set()
        for file in potential_dups:
            one = self.file_path(file)
            two = batch.file_path(file)
            if filecmp.cmp(one, two, shallow=False):
                dups.add(file)
            else:
                self.logger.warning(f"Not the same? one: {one}, two: {two}")

        return new_docs - dups

    def counts(self) -> str:
        """
        Returns a summary of unique vs duplicate document count
        """
        return f"Total: {len(self)}, Uniques: {len(self.uniques)}, Dups: {self.dups()}"

    def dups(self) -> int:
        """
        Returns a count of duplicate entries
        """
        return len(self) - len(self.uniques)
