import pytest

from prescan.batch_loader import BatchLoader
from tests.test_constants import BATCH_NAMES, BATCHES, TEST_DATA_DIR


def test_batch_loader_invalid_input():
    with pytest.raises(Exception) as pytest_error:
        BatchLoader("missing-dir")

    assert pytest_error.value.args[0] == "Specified input directory is missing"


def test_batch_loader_loads_files():
    loader = BatchLoader(TEST_DATA_DIR)
    assert 2 == len(loader.batches)
    assert BATCH_NAMES == {batch.name for batch in loader.batches}
    assert BATCHES['faxes-1'] == loader.batches[0].faxes
    assert BATCHES['faxes-2'] == loader.batches[1].faxes
