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