# Take-Home Challenge
Take-Home Challenge for Crisp Interview Process

## Project Summary
This project implements a synchronous, configurable csv cleaning mechanism in Python. It optimizes for a very small memory footprint and highly configurable and extensible transformations. The primary workhorse function, [clean_csv](./csv_cleaner/csv_cleaner.py), is a generator, enabling clients to decide what to do with each transformed row based on contents, success, etc. Transformations are detailed in a simple json structure and the addition of new transformation types requires only modifying a single existing file.

## Setup
- This project was developed using WSL2 - Ubuntu 22.04.1 LTS as an OS.
- [asdf](https://asdf-vm.com/) and [direnv](https://direnv.net/) were used to manage the Python environment.
- In the absence of asdf and direnv, the project can also be setup by:
    1. Installing the python version specified in [.tool-versions](./.tool-versions)
    2. Creating and activating a venv for the project: `python -m venv ./venv` and `source ./venv/bin/activate`
    3. Installing the [requirements](./requirements.txt) via pip: `pip install -r {repo-root}/requirements.txt`
- After following either setup method, you should be able to confirm proper setup by running the test suite. From repo root: `pytest`.
- Additionally, you can `cd ./examples` and run the example client scripts.

## Utilization
To make use of the csv_cleaner, the user will need to provide 2 arguments to the `clean_csv` function from [csv_cleaner](./csv_cleaner/csv_cleaner.py): the path to the csv data file and a configuration dictionary that adheres to the below schema. The latter can also be obtained by supplying a path to a json configuration file to the `get_config_from_file` function in [csv_cleaner](./csv_cleaner/csv_cleaner.py). The `clean_csv` function will yield each row that it processes, starting with the header row, as well as a boolean success status for the processing of that row, and a failure tuple comprised of the original row and an exception message if there was a failure encountered during the processing of the row.

Configuration Schema:
```
{
    "column_definitions": {
        "output_column_name_1": {
            "first_transform_function_name": {
                "transform_arg_1": "",
                "transform_arg_2": "",
                ...
            },
            "second_transform_function_name": {
                "transform_arg_1": "",
                "transform_arg_2": "",
                ...
            },
            ...
        }
        "output_column_name_2": {
            ...
        },
        ...
    }
}
```
Currently, the following 4 transform functions are provided:
1. source: outputs the specified literal or a value from the specified field on the original row. Args are:
    1. literal: string
    2. field: string
2. concatenate: outputs the result of concatenating the values from supplied fields on the original row using an optional separator. Args:
    1. fields: array\<string\>
    2. separator: string
3. parse: outputs the result of attempting to parse the specified data type from the previous transformation's result. Args:
    1. type: string
4. proper_case: outputs the result of proper casing the previous transformation's result. No arguments.

Additional transform functions can be added by:
1. Creating a new file in [./transforms](./transforms/)
2. Defining a transform function that returns a scalar value inside the new file. The function should accept the following args:
    1. cell_value: the output of the previous transform
    2. row: the original row of data
    3. header_row: the original header row
    4. transform_config: the configuration for this transform
3. `import`ing the new function in [\_\_init\_\_.py](./transforms/__init__.py)




## Project Structure
- [csv_cleaner/csv_cleaner.py](./csv_cleaner/csv_cleaner.py) is the primary module containing the highest level of abstraction over the csv cleaning process. Clients should import `clean_csv` and optionally `get_config_from_file` from the `csv_cleaner` package to make use of the core functionality.
- [tests](./tests/) contains the `pytest` test suite for the project. It is split into two groups, based on the project's submodules: [transforms](./tests/transforms/) and [csv_cleaner](./tests/csv_cleaner/). The latter's tests behave more like integration tests than unit tests.
- [data](./data/) contains example .csv files to use during development and testing.
- [configs](./configs/) contains example json configurations to use during development and testing.
- [examples](./examples/) contains a few sample scripts that act as a client making use of the project's functionality.

## Architectural Decisions

### Synchronous Iteration
This project uses 'csv' from the Python Standard Library as a means of parsing the csv file. For simplicity's sake, rows are processed in a synchronous and iterative fashion. Making use of multi-processing to process several small batches of rows simultaneously would be an excellent evolution of the product, especially given the requirement of processing very large files. Set-based approaches such as **1.**\) use of duckdb to treat the csv file as an in-memory sql table or **2.**\) use of pandas for vectorized transformations were considered, but both would significantly increase the memory appetite of the application. Additionally, use of these comparatively heavy-weight packages seemed to violate the spirit of the exercise.

### Use of `globals()`
The secret sauce of the extensible transformations is a combination of this and the following architectural decisons. In the [transform_row](./csv_cleaner/csv_cleaner.py) function, clever use of `globals()` and the transformation name supplied in the json configuration file allow us to avoid tight-coupling of the available transformations to the csv_cleaner itself. This prevents the need to make edits to the csv_cleaner when adding additional transformations. Instead, users can define and "export" (via [\_\_init\_\_.py](./transforms/__init__.py)) additional transform functions and immediately reference them in their json configuration.

### Use of Transform Function Names in the JSON Configuration File
For any given output column, the required transformations are defined in a json dictionary. This provides a very readable, easily modified means of describing necessary data transformations. Each key in the dictionary must also be the name of a supplied transformation in [transforms](./transforms/).

## Assumptions
1. csv files can be parsed using the "excel" style from the `csv` package in Python's Standard Library.
2. Every data file has exactly one header row and it is the first row in the file.
3. User would prefer to choose what to do with the cleaned rows, potentially on a per row basis.
4. All rows have the same number of columns and this matches the column count of header row.

## Backlog

- Validate each row's column count against the header row
- Validate config. Make sure transforms actually exist
- Multi-processing of rows
- Clean up examples (reduce dupe code, etc.)
- Support for streams from S3, ADLSg2, etc.
- Allow for specifying the original data set's header row in config
- Make the transform functions' contract official (or unnecessary). Potentially includes making a nice context object to pass around instead of the current 4 argument signature.
- Support for additional delimited file formats via the json configuration
- Additional transforms (like replace, arithmetic, etc.)
- Support more date formats
- detailed instructions for setup of asdf and direnv
