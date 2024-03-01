def source(cell_value, row, header_row, transform_config):
    value = None

    if 'field' in transform_config:
        field = transform_config['field']
        position = header_row.index(field)
        value = row[position]
    elif 'literal' in transform_config:
        value = transform_config['literal']
    else:
        raise Exception(f"Source transform misconfigured: {transform_config}")
    
    return value