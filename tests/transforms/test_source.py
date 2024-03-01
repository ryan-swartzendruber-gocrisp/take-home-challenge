import os
import sys
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from transforms import source

class TestSource:
    def __get_args(self):
        cell_value = None
        row = [1, 2, 3]
        header_row = ["Col1", "Col2", "Col3"]

        return cell_value, row, header_row

    def test_source_with_field(self):
        cell_value, row, header_row = self.__get_args()

        transform_config = {
            "field": "Col2"
        }

        result = source(cell_value, row, header_row, transform_config)

        assert result == 2

    def test_source_with_literal(self):
        cell_value, row, header_row = self.__get_args()

        transform_config = {
            "literal": "crisp is cool"
        }

        result = source(cell_value, row, header_row, transform_config)

        assert result == "crisp is cool"

    def test_source_with_bad_config(self):
        cell_value, row, header_row = self.__get_args()

        transform_config = {}

        with pytest.raises(Exception):
            result = source(cell_value, row, header_row, transform_config)


