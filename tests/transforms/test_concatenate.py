import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from transforms import concatenate

class TestConcatenate:
    def __get_args(self):
        cell_value = None
        row = ["oh,", "you", "think", "darkness", "is", "your", "ally"]
        header_row = ["Col1", "Col2", "Col3", "Col4", "Col5", "Col6", "Col7"]
        
        return cell_value, row, header_row

    def test_concatenate_no_separator_in_config(self):
        cell_value, row, header_row = self.__get_args()
        
        transform_config = {
            "fields": ["Col1", "Col2", "Col3", "Col4", "Col5", "Col6", "Col7"]
        }

        result = concatenate(cell_value, row, header_row, transform_config)

        assert result == "oh, you think darkness is your ally"

    def test_concatenate_no_separator_in_config(self):
        cell_value, row, header_row = self.__get_args()
        
        transform_config = {
            "fields": ["Col1", "Col2", "Col3", "Col4", "Col5", "Col6", "Col7"],
            "separator": "-"
        }

        result = concatenate(cell_value, row, header_row, transform_config)

        assert result == "oh,-you-think-darkness-is-your-ally"

    def test_concatenate_no_fields_in_config(self):
        cell_value, row, header_row = self.__get_args()
        
        transform_config = {}

        with pytest.raises(Exception):
            result = concatenate(cell_value, row, header_row, transform_config)
