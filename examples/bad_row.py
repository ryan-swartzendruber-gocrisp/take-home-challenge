import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from csv_cleaner import get_config_from_file, clean_csv

config = get_config_from_file('../configs/example.json')

for row, is_successfully_processed_row, failure in clean_csv('../data/bad_row.csv', config):
    if not is_successfully_processed_row:
        print(failure)
    else:
        print(row)