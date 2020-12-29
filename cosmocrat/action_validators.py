import os
import re
import argparse
import cosmocrat.definitions as definitions

class validate_input_path(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        input_file_path = values
        if not os.path.isfile(input_file_path):
            raise argparse.ArgumentTypeError(f'validate_input_path: {input_file_path} is not a valid path')
        if not os.access(input_file_path, os.R_OK):
            raise argparse.ArgumentTypeError(f'validate_input_path: {input_file_path} is not a readable file')
        setattr(namespace, self.dest, input_file_path)

class validate_output_path(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        output_file_path = values
        output_dir = os.path.dirname(output_file_path)
        if not os.access(output_dir, os.W_OK):
            raise argparse.ArgumentTypeError(f'validate_output_path: {output_file_path} is not a valid output path')
        setattr(namespace, self.dest, output_file_path)

class validate_timestamp(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        timestamp = values
        if not re.match(definitions.TIMESTAMP_REGEX, timestamp):
            raise argparse.ArgumentTypeError(f'validate_timestamp: {timestamp} is not a valid timestmap')
        setattr(namespace, self.dest, timestamp)