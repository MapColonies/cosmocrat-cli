import os
import re
import argparse
import validators
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

class validate_time_units_limit(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        time_units = values
        for time_unit in time_units:
            if time_unit not in definitions.Time_Unit._member_names_:
                raise argparse.ArgumentTypeError(f'validate_time_units_limit: {time_unit} is not a valid time unit')
        setattr(namespace, self.dest, time_units)

class validate_url(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        url = values
        if not validators.url(url):
            raise argparse.ArgumentTypeError(f'validate_url: {url} is not a valid url')
        setattr(namespace, self.dest, url)
