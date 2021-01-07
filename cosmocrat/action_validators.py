import os
import re
import argparse
import validators
import cosmocrat.definitions as definitions

from cosmocrat.helper_functions import is_iterable
from abc import ABC as AbstractBaseClass, abstractmethod

class validate_base(AbstractBaseClass, argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        value_to_validate = values
        self.validate(value_to_validate)
        setattr(namespace, self.dest, value_to_validate)

    @abstractmethod
    def validate(self, value):
        pass

class validate_input_path(validate_base):
    def validate(self, input_file_path):
        if not os.path.isfile(input_file_path):
            raise argparse.ArgumentTypeError(f'validate_input_path: {input_file_path} is not a valid path')
        if not os.access(input_file_path, os.R_OK):
            raise argparse.ArgumentTypeError(f'validate_input_path: {input_file_path} is not a readable file')

class validate_output_path(validate_base):
    def validate(self, output_file_path):
        output_dir = os.path.dirname(output_file_path)
        if not os.access(output_dir, os.W_OK):
            raise argparse.ArgumentTypeError(f'validate_output_path: {output_file_path} is not a valid output path')

class validate_timestamp(validate_base):
    def validate(self, timestamp):
        if not re.match(definitions.TIMESTAMP_REGEX, timestamp):
            raise argparse.ArgumentTypeError(f'validate_timestamp: {timestamp} is not a valid timestmap')

class validate_time_units_limit(validate_base):
    def validate(self, time_units):
        if not is_iterable(time_units):
            raise argparse.ArgumentTypeError(f'validate_time_units_limit: {time_units} is not iterable')
        for time_unit in time_units:
            if time_unit not in definitions.Time_Unit._member_names_:
                raise argparse.ArgumentTypeError(f'validate_time_units_limit: {time_unit} is not a valid time unit')

class validate_url(validate_base):
    def validate(self, url):
        try:
            validators.url(url)
        except (TypeError, Exception):
            raise argparse.ArgumentTypeError(f'validate_url: {url} is not a valid url')
