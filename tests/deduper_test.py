import pytest

from prescan.deduper import Deduper
from prescan.document_batch import DocumentBatch
from tests.test_constants import (
    BATCH_1,
    BATCH_1_DIR,
    BATCH_1_OUTPUT_DIR,
    BATCH_2,
    BATCH_2_DIR,
    BATCH_2_OUTPUT_DIR,
    BATCHES,
)


@pytest.fixture
def deduper():
    batches = [
        DocumentBatch(BATCH_1, BATCH_1_DIR, BATCH_1_OUTPUT_DIR),
        DocumentBatch(BATCH_2, BATCH_2_DIR, BATCH_2_OUTPUT_DIR),
    ]
    return Deduper(batches=batches)


def test_get_unique_docs(deduper):
    docs = deduper.get_unique_docs()
    assert len(docs) == 2
    assert docs[0].uniques == BATCHES[BATCH_1]
    assert docs[1].uniques == BATCHES[BATCH_2] - BATCHES[BATCH_1]
