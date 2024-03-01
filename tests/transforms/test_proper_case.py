import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from transforms import proper_case

class TestProperCase:
    def __get_args(self):
        row = []
        header_row = []
        transform_config = {}

        return row, header_row, transform_config

    def test_proper_case(self):
        row, header_row, transform_config = self.__get_args()
        
        cell_value = "sir dingus"

        result = proper_case(cell_value, row, header_row, transform_config)

        assert result == "Sir Dingus"