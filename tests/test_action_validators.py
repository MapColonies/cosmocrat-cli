import pytest
import argparse
import unittest.mock as mock
import cosmocrat.argument_parser.validation.action_validators as validators

from tests.helpers.helpers import get_current_datetime, datetime_to_string
from tests.definitions import FULL_FILE_PATH, FILE_PATH, FILE_NAME, FILE_FORMAT, FAKE_MULTI_PURPOSE

@pytest.fixture
def input_path_validator():
    '''Returns an empty validate_input_path'''
    return validators.validate_input_path(None, None)

@pytest.fixture
def output_path_validator():
    '''Returns an empty validate_output_path'''
    return validators.validate_output_path(None, None)

@pytest.fixture
def timestamp_validator():
    '''Returns an empty validate_timestamp'''
    return validators.validate_timestamp(None, None)

@pytest.fixture
def time_units_limit_validator():
    '''Returns an empty validate_time_units_limit'''
    return validators.validate_time_units_limit(None, None)

@pytest.fixture
def url_validator():
    '''Returns an empty validate_url'''
    return validators.validate_url(None, None)

@pytest.fixture
def expected_argument_type_error():
    '''Returns an expect for raised ArgumentTypeError'''
    return pytest.raises(argparse.ArgumentTypeError)

@pytest.mark.validators
class TestValidators():
    def test_validate_input_path(self, input_path_validator):
        with mock.patch('os.path.isfile', return_value=True), \
        mock.patch('os.access', return_value=True):
            assert input_path_validator.validate(input_file_path=FULL_FILE_PATH) is None

    def test_validate_input_path_raises_exception(self, input_path_validator, expected_argument_type_error):
        with mock.patch('os.path.isfile', return_value=False), expected_argument_type_error:
            input_path_validator.validate(input_file_path=FAKE_MULTI_PURPOSE)
        with mock.patch('os.path.isfile', return_value=True), \
        mock.patch('os.access', return_value=False), \
        expected_argument_type_error:
            input_path_validator.validate(input_file_path=FAKE_MULTI_PURPOSE)

    def test_validate_output_path(self, output_path_validator):
        with mock.patch('os.access', return_value=True):
            assert output_path_validator.validate(output_file_path=FULL_FILE_PATH) is None

    def test_validate_output_path_raises_exception(self, output_path_validator, expected_argument_type_error):
        with mock.patch('os.access', return_value=False), expected_argument_type_error:
            output_path_validator.validate(output_file_path=FAKE_MULTI_PURPOSE)

    def test_validate_timestamp(self, timestamp_validator):
        now = datetime_to_string(get_current_datetime())
        assert timestamp_validator.validate(timestamp=now) is None

    def test_validate_timestamp_raises_exception(self, timestamp_validator, expected_argument_type_error):
        with expected_argument_type_error:
            timestamp_validator.validate(timestamp=FAKE_MULTI_PURPOSE)

    def test_validate_time_units_limit(self, time_units_limit_validator):
        for case in [['day'], ['day', 'week', 'hour'], []]:
            assert time_units_limit_validator.validate(time_units=case) is None

    def test_validate_time_units_limit_raises_exception(self, time_units_limit_validator, expected_argument_type_error):
        for case in [None, 'day', ['year']]:
            with expected_argument_type_error:
                time_units_limit_validator.validate(time_units=case)

    def test_validate_url_raises_exception(self, url_validator, expected_argument_type_error):
        for case in [None, FAKE_MULTI_PURPOSE]:
            with expected_argument_type_error:
                url_validator.validate(url=case)
