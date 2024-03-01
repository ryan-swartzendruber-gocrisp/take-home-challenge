import os
import sys
import pytest
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from transforms import parse

class TestParse:
    def __get_args(self):
        row = []
        header_row = []

        return row, header_row

    def test_parse_an_int(self):
        row, header_row = self.__get_args()
        
        cell_value = "1"

        transform_config = {
            "type": "int"
        }

        result = parse(cell_value, row, header_row, transform_config)

        assert result == 1
    
    def test_parse_a_string(self):
        row, header_row = self.__get_args()
        
        cell_value = "crisp"

        transform_config = {
            "type": "string"
        }

        result = parse(cell_value, row, header_row, transform_config)

        assert result == "crisp"

    def test_parse_a_float(self):
        row, header_row = self.__get_args()
        
        cell_value = "100,000.00"

        transform_config = {
            "type": "float"
        }

        result = parse(cell_value, row, header_row, transform_config)

        assert result == 100000.00

    def test_parse_a_datetime(self):
        row, header_row = self.__get_args()
        
        cell_value = "2024-03-11"

        transform_config = {
            "type": "datetime"
        }

        result = parse(cell_value, row, header_row, transform_config)

        assert result == datetime(2024, 3, 11)

    def test_parse_bad_type(self):
        row, header_row = self.__get_args()
        
        cell_value = "100"

        transform_config = {
            "type": "crisp"
        }

        with pytest.raises(Exception):
            result = parse(cell_value, row, header_row, transform_config)

    def test_parse_bad_config(self):
        row, header_row = self.__get_args()
        
        cell_value = "100"

        transform_config = {}

        with pytest.raises(Exception):
            result = parse(cell_value, row, header_row, transform_config)



