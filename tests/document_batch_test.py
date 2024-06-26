import pytest

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
def batch_1():
    return DocumentBatch(BATCH_1, BATCH_1_DIR, BATCH_1_OUTPUT_DIR)


@pytest.fixture
def batch_2():
    return DocumentBatch(BATCH_2, BATCH_2_DIR, BATCH_2_OUTPUT_DIR)


def test_constructor_sets_name(batch_1):
    assert batch_1.name == BATCH_1


def test_constructor_sets_path(batch_1):
    assert batch_1.path == BATCH_1_DIR


def test_constructor_sets_output_dir_path(batch_1):
    assert BATCH_1_OUTPUT_DIR == batch_1.output_dir_path


def test_constructor_sets_faxes(batch_1):
    assert batch_1.faxes == BATCHES[BATCH_1]


def test_constructor_inits_uniques_with_faxes(batch_1):
    assert batch_1.uniques == BATCHES[BATCH_1]


def test_file_path_returns_path_to_file(batch_1):
    assert batch_1.file_path("somefile.pdf") == f"{BATCH_1_DIR}/somefile.pdf"


def test_filter_all_duplicates_returns_unique_docs(batch_1, batch_2):
    assert len(batch_2.uniques) == 5

    filtered_batch = batch_2.filter_all_duplicates_in([batch_1])

    assert len(filtered_batch.uniques) == 3


def test_dups_returns_duplicate_count(batch_1):
    batch_1.uniques = {"MEDHIS.PDF"}

    assert len(batch_1.faxes) == 3
    assert len(batch_1.uniques) == 1
    assert batch_1.dups() == 2


def test_has_outputs_when_dir_exists(batch_1):
    assert batch_1.has_outputs


def test_has_outputs_when_dir_absent(batch_2):
    assert not batch_2.has_outputs
