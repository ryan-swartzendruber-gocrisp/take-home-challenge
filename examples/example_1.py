import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from csv_cleaner import get_config_from_file, clean_csv

config = get_config_from_file('../configs/example.json')

for row in clean_csv('../data/example.csv', config):
    print(row)