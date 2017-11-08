#!/usr/bin/python
"""Square root of all numeric values in a column file."""
import argparse as ap
import csv
import math
from array import array

from dit_flow.dit_widget.common.setup_logger import setup_logger, DEFAULT_LOG_LEVEL


def math_square_root(missing_value, input_data_file=None, output_data_file=None, log_file=None, log_level=DEFAULT_LOG_LEVEL):
    # Square root of all values in input_data_file and writes result to
    # output_data_file.
    logger = setup_logger(__name__, log_file, log_level)
    assert input_data_file is not None, 'An input CSV file with columns of values.'
    assert output_data_file is not None, 'An output CSV file to write new values.'
    with open(input_data_file, newline='') as _in, \
            open(output_data_file, 'w', newline='') as _out:
            logger.info('Square root of values in column')
            output = csv.writer(_out)
            reader = csv.reader(_in)
            for line in reader:
                new_line = array('f')
                for item in line:
                    if (float(item) != float(missing_value)) and (float(item) >= 0.0):
                        value = math.sqrt(float(item))
                    else:
                        value = float(missing_value)
                    new_line.append(value)
                output.writerow(['{:.2f}'.format(x) for x in new_line])


def parse_arguments():
    parser = ap.ArgumentParser(description="Square root of all values in "
                               "input_data_file and writes the result to "
                               "output_data_file.")

    parser.add_argument('missing_value', type=float, help='Missing data value in file.')

    parser.add_argument('-i', '--input_data_file',
                        help='Step file containing input data to manipulate.')
    parser.add_argument('-o', '--output_data_file', help='Step file to store output data.')
    parser.add_argument('-l', '--log_file', help='Step file to collect log information.')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    math_square_root(args.missing_value,
                     args.input_data_file, args.output_data_file, args.log_file)
