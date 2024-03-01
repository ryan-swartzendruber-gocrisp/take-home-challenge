import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from csv_cleaner.csv_cleaner import transform_row

class TestTransformRow:
    def test_transform_row_no_errors(self):
        row = ["a", "b", "c"]
        header_row = ["Col1", "Col2", "Col3"]
        column_definitions =  {
            "Col1String": {
                "source": {
                    "field": "Col1"
                },
                "parse": {
                    "type": "str"
                }
            }
        }

        new_row, is_successfully_processed_row, failure = transform_row(row, header_row, column_definitions)
        assert (new_row, is_successfully_processed_row, failure) == (['a'], True, None)

    def test_transform_row_with_errors(self):
        row = ["a", "b", "c"]
        header_row = ["Col1", "Col2", "Col3"]
        column_definitions =  {
            "Col1Int": {
                "source": {
                    "field": "Col1"
                },
                "parse": {
                    "type": "int"
                }
            }
        }

        new_row, is_successfully_processed_row, failure = transform_row(row, header_row, column_definitions)
        assert (new_row, is_successfully_processed_row, failure[0]) == ([], False, row)

