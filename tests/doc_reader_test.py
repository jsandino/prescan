import pytest

from prescan.doc_reader import DocReader
from tests.test_constants import BATCH_1_OUTPUT_DIR, NON_PRESCRIPTIONS, PRESCRIPTIONS, TEST_OUTPUT_DIR

def test_is_prescription_for_presc_pdfs():
  for pdfFile in PRESCRIPTIONS:
    reader = DocReader(pdfFile, TEST_OUTPUT_DIR)
    assert reader.is_prescription() == True


def test_is_prescription_for_non_presc_pdfs():
  for pdfFile in NON_PRESCRIPTIONS:
    reader = DocReader(pdfFile, TEST_OUTPUT_DIR)
    assert reader.is_prescription() == False


def test_get_output_file_path_for_prescription():
  input_file_path = PRESCRIPTIONS[0]
  file_name = input_file_path.split("/")[-1]
  reader = DocReader(input_file_path, BATCH_1_OUTPUT_DIR)
  output_file = reader.get_output_file_path("batch1", file_name)
  assert output_file == f"{BATCH_1_OUTPUT_DIR}/presc/" + file_name


def test_get_output_file_path_for_non_prescription():
  input_file_path = NON_PRESCRIPTIONS[0]
  file_name = input_file_path.split("/")[-1]
  reader = DocReader(input_file_path, BATCH_1_OUTPUT_DIR)
  output_file = reader.get_output_file_path("batch1", file_name)
  assert output_file == f"{BATCH_1_OUTPUT_DIR}/non-presc/" + file_name