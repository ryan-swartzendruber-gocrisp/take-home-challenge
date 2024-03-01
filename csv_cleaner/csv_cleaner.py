import csv
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from transforms import source, parse, concatenate, proper_case

def clean_csv(path_to_file: str, config):
    has_header_row, column_definitions = parse_config(config)

    with open(path_to_file, "r") as file:
        reader = csv.reader(file)
        if has_header_row:
            header_row = next(reader)
            cleaned_header_row = [k for k, v in column_definitions.items()]
            yield cleaned_header_row, True, None
        
        for row in reader:
            cleaned_row, is_successfully_processed_row, failure = transform_row(row, header_row, column_definitions)
            yield cleaned_row, is_successfully_processed_row, failure
            
def get_config_from_file(path_to_file: str):
    with open(path_to_file, "r") as file:
        return json.load(file)

def parse_config(config):
    has_header_row = False
    if 'has_header_row' in config:
        has_header_row = config['has_header_row']
    
    column_definitions = {}
    if 'column_definitions' in config:
        column_definitions = config['column_definitions']
    
    return has_header_row, column_definitions

def transform_row(row, header_row, column_definitions):
    new_row = []
    is_successfully_processed_row = True
    failure = None

    try:
        for output_column, transforms in column_definitions.items():
            cell_value = None
            try: 
                for name, transform_config in transforms.items():
                        cell_value = globals()[name](cell_value, row, header_row, transform_config)
            except Exception as e:
                raise Exception(f"output_column: {output_column}, transform: {name}, exception: {str(e)}")

            new_row.append(cell_value)
    except Exception as e:
        is_successfully_processed_row = False
        failure = (row, str(e))

    return new_row, is_successfully_processed_row, failure

