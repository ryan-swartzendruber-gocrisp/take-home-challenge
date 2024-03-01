from datetime import datetime

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