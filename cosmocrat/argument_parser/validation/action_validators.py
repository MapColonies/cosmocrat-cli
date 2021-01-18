import os
import re
import argparse
import validators
import cosmocrat.definitions as definitions

from cosmocrat.helper_functions import is_iterable
from cosmocrat.argument_parser.validation.base_action_validator import BaseActionValidator

class validate_input_path(BaseActionValidator):
    def validate(self, input_file_path):
        if not os.path.isfile(input_file_path):
            raise argparse.ArgumentTypeError(f'validate_input_path: {input_file_path} is not a valid path')
        if not os.access(input_file_path, os.R_OK):
            raise argparse.ArgumentTypeError(f'validate_input_path: {input_file_path} is not a readable file')

class validate_output_path(BaseActionValidator):
    def validate(self, output_file_path):
        output_dir = os.path.dirname(output_file_path)
        if not os.access(output_dir, os.W_OK):
            raise argparse.ArgumentTypeError(f'validate_output_path: {output_file_path} is not a valid output path')

class validate_timestamp(BaseActionValidator):
    def validate(self, timestamp):
        if not re.match(definitions.TIMESTAMP_REGEX, timestamp):
            raise argparse.ArgumentTypeError(f'validate_timestamp: {timestamp} is not a valid timestmap')

class validate_time_units_limit(BaseActionValidator):
    def validate(self, time_units):
        if not is_iterable(time_units):
            raise argparse.ArgumentTypeError(f'validate_time_units_limit: {time_units} is not iterable')
        for time_unit in time_units:
            if time_unit not in definitions.Time_Unit._member_names_:
                raise argparse.ArgumentTypeError(f'validate_time_units_limit: {time_unit} is not a valid time unit')

class validate_url(BaseActionValidator):
    def validate(self, url):
        try:
            if validators.url(url) is not True:
                raise TypeError
        except (TypeError, Exception):
            raise argparse.ArgumentTypeError(f'validate_url: {url} is not a valid url')
