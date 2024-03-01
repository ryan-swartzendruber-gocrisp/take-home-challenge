import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from csv_cleaner import get_config_from_file, clean_csv

config = get_config_from_file('../configs/example.json')

good = []
bad = []

for row, is_successfully_processed_row, failure in clean_csv('../data/mix_of_good_and_bad.csv', config):
    if not is_successfully_processed_row:
        bad.append(failure)
    else:
        good.append(row)

print("Successes")
[print(row) for row in good]

print("Failures")
[print(failure) for failure in bad]