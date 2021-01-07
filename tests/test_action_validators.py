import pytest
import argparse
from tests.helpers.helper_functions import get_current_datetime, datetime_to_string

import cosmocrat.action_validators as validators

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

# TODO: find if possible:
# region get_fixture_from_parametrize

# @pytest.fixture(params=[validate_input_path, validate_output_path])
# def validator(request):
#     return request.param(None, None)

# @pytest.mark.parametrize("value, expected", [
#     ('/tmp/cosmocrat-cli/data/results/output2.osm.pbf', None)
# ])
# def test_foo(validator, value, expected):
#     print(validator)
#     assert validator.validate(value) is expected

# @pytest.mark.parametrize("value, expected, validator", [
#     ('/tmp/cosmocrat-cli/data/results/output2.osm.pbf', None, 'input_path_validator')
# ], indirect=['validator'])
# def test_valid(input_path_validator, value, expected, validator):
#     print('!!!')
#     print(validator)
#     print(input_path_validator)
#     assert input_path_validator.validate(value) is expected

# endregion

@pytest.mark.validators
class TestValidators():
    def test_validate_input_path(self, input_path_validator):
        assert input_path_validator.validate(input_file_path='/tmp/cosmocrat-cli/data/results/output2.osm.pbf') is None

    def test_validate_input_path_raises_exception(self, input_path_validator):
        with pytest.raises(argparse.ArgumentTypeError):
            input_path_validator.validate(input_file_path='non_exist_path')

    def test_validate_output_path(self, output_path_validator):
        assert output_path_validator.validate(output_file_path='/tmp/cosmocrat-cli/data/output.osc') is None

    def test_validate_output_path_raises_exception(self, output_path_validator):
        with pytest.raises(argparse.ArgumentTypeError):
            output_path_validator.validate(output_file_path='non_exist_path')

    def test_validate_timestamp(self, timestamp_validator):
        now = datetime_to_string(get_current_datetime())
        assert timestamp_validator.validate(timestamp=now) is None

    def test_validate_timestamp_raises_exception(self, timestamp_validator):
        with pytest.raises(argparse.ArgumentTypeError):
            timestamp_validator.validate(timestamp='invalid_timestamp')

    def test_validate_time_units_limit(self, time_units_limit_validator):
        assert time_units_limit_validator.validate(time_units=['day']) is None
        assert time_units_limit_validator.validate(time_units=['day', 'week', 'hour']) is None
        assert time_units_limit_validator.validate(time_units=[]) is None

    def test_validate_time_units_limit_raises_exception(self, time_units_limit_validator):
        with pytest.raises(argparse.ArgumentTypeError):
            time_units_limit_validator.validate(time_units=None)
            time_units_limit_validator.validate(time_units='day')
            time_units_limit_validator.validate(time_units=['year'])

    def test_validate_url_raises_exception(self, url_validator):
        with pytest.raises(argparse.ArgumentTypeError):
            url_validator.validate(url=None)
            url_validator.validate(url='invalid_url')
