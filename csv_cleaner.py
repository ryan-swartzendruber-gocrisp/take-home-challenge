import csv
import json
import string
from datetime import datetime
from itertools import dropwhile, takewhile

def loop_over_csv(path_to_file: str, config):
    header_row_count, column_definitions = parse_config(config)

    with open(path_to_file, "r") as file:
        reader = csv.reader(file)
        rows_processed_count = 0
        header_row = []
        
        for row in reader:
            if rows_processed_count >= header_row_count:
                cleaned_row = transform_row(row, header_row, column_definitions)
                yield cleaned_row
            else:
                header_row = row
            
            rows_processed_count += 1

def get_config_from_file(path_to_file: str):
    with open(path_to_file, "r") as file:
        return json.load(file)

def parse_config(config):
    header_row_count = 0
    if 'header_row_count' in config:
        header_row_count = config['header_row_count']
    
    column_definitions = {}
    if 'column_definitions' in config:
        column_definitions = config['column_definitions']
    
    return header_row_count, column_definitions

def transform_row(row, header_row, column_definitions):
    new_row = []
    for _, transforms in column_definitions.items():
        cell_value = None
        for name, transform_config in transforms.items():
            cell_value = globals()[name](cell_value, row, header_row, transform_config)

        new_row.append(cell_value)
    
    return new_row

def source(cell_value, row, header_row, transform_config):
    value = None

    if 'field' in transform_config:
        field = transform_config['field']
        position = header_row.index(field)
        value = row[position]
    elif 'literal' in transform_config:
        value = literal
    else:
        raise Exception(f"Source transform misconfigured: {transform_config}")
    
    return value

def parse(cell_value, row, header_row, transform_config):
    value = cell_value

    if 'type' in transform_config:
        data_type = transform_config['type']

        if data_type in ['integer', 'int']:
            value = int(value)
        elif data_type in ['string', 'str']:
            value = str(value)
        elif data_type == 'float':
            value = float(value.replace(',',''))
        elif data_type == 'datetime':
            value = datetime.strptime(value, '%Y-%m-%d')
        else:
            raise Exception(f"Parse transformation does not support this type: {transform_config}")
    else:
        raise Exception(f"Parse transformation requires 'type': {transform_config}")
    
    return value

def concatenate(cell_value, row, header_row, transform_config):
    fields = None
    if 'fields' in transform_config:
        fields = transform_config['fields']
    else:
        raise Exception(f"Concatenate transform requires 'fields' array: {transform_config}")

    separator = ' '
    if 'separator' in transform_config:
        separator = transform_config['separator']
    
    values = []

    for field in fields:
        position = header_row.index(field)
        values.append(row[position])

    return separator.join(values)

def proper_case(cell_value, row, header_row, transform_config):
    return string.capwords(cell_value)

config = get_config_from_file('./configs/parse_float.json')

for row in loop_over_csv('./data/example.csv', config):
    print(row)

