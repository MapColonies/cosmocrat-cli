import pytest
from os.path import join

import cosmocrat.definitions as definitions
import cosmocrat.helper_functions as helpers
from tests.helpers.helper_functions import get_current_datetime, datetime_to_string
from random import randrange
from datetime import datetime, timedelta

EMPTY_STRING=''
FILE_PATH='/tmp/cosmocrat-cli/data'
FILE_NAME='output'
FILE_FORMAT='osm.pbf'
FAKE_MULTI_PURPOSE='xyz'

def test_get_compression_method():
    assert helpers.get_compression_method(False) == ('none', EMPTY_STRING)
    assert helpers.get_compression_method(True) == ('gzip', '.gz')

    assert helpers.get_compression_method(False, FILE_FORMAT) == ('none', FILE_FORMAT)
    assert helpers.get_compression_method(True, FILE_FORMAT) == ('gzip', f'{FILE_FORMAT}.gz')

    assert helpers.get_compression_method(False, FILE_FORMAT, 'bz2') == ('none', FILE_FORMAT)
    assert helpers.get_compression_method(True, FILE_FORMAT, FAKE_MULTI_PURPOSE) == ('none', FILE_FORMAT)
    assert helpers.get_compression_method(True, FILE_FORMAT, 'bz2') == \
        (definitions.COMPRESSION_METHOD_MAP.get('bz2'), f'{FILE_FORMAT}.bz2')

def test_deconstruct_file_path():
    assert helpers.deconstruct_file_path(EMPTY_STRING) == (None, EMPTY_STRING, [], None)

    name_and_format = f'{FILE_NAME}.{FILE_FORMAT}'
    assert helpers.deconstruct_file_path(join(FILE_PATH, name_and_format)) == \
        (FILE_PATH, FILE_NAME, [], FILE_FORMAT)

    timestamp = datetime_to_string(get_current_datetime())
    assert helpers.deconstruct_file_path(join(FILE_PATH, timestamp)) == (FILE_PATH, EMPTY_STRING, [timestamp], None)
    assert helpers.deconstruct_file_path(join(FILE_PATH, f'{timestamp}.{name_and_format}')) \
        == (FILE_PATH, FILE_NAME, [timestamp], FILE_FORMAT)

@pytest.mark.parametrize("value, successful, output_format, rest", [
    (EMPTY_STRING, False, None, EMPTY_STRING),
    (FILE_PATH, False, None, FILE_PATH),
    (join(FILE_PATH, f'{FILE_NAME}.{FILE_FORMAT}'),
        True, FILE_FORMAT, join(FILE_PATH, FILE_NAME)),
    (f'{FILE_NAME}.{FILE_FORMAT}', True, FILE_FORMAT, FILE_NAME),
    (f'{FILE_NAME}.{FAKE_MULTI_PURPOSE}', False, None, f'{FILE_NAME}.{FAKE_MULTI_PURPOSE}')
])
def test_get_file_format(value, successful, output_format, rest):
    assert helpers.get_file_format(value) == (successful, output_format, rest)

def test_get_file_dir():
    assert helpers.get_file_dir(EMPTY_STRING) == (False, None, EMPTY_STRING)
    assert helpers.get_file_dir(FILE_NAME) == (False, None, FILE_NAME)
    assert helpers.get_file_dir(FILE_PATH + '/') == (True, FILE_PATH, EMPTY_STRING)
    assert helpers.get_file_dir(join(FILE_PATH, FILE_NAME)) == (True, FILE_PATH, FILE_NAME)

def test_remove_dots_from_edges_of_string():
    get_random_dots = lambda: '.' * randrange(10)
    assert helpers.remove_dots_from_edges_of_string(get_random_dots()) == EMPTY_STRING

    string_value = 'c.osm.ocrat'
    assert helpers.remove_dots_from_edges_of_string(f'{get_random_dots()}{string_value}{get_random_dots()}') == string_value

def test_get_file_timestamps():
    base_input = FAKE_MULTI_PURPOSE
    assert helpers.get_file_timestamps(base_input) == (False, [], base_input)

    datetime = get_current_datetime()
    timestamp = datetime_to_string(datetime)
    assert helpers.get_file_timestamps(timestamp) == (True, [timestamp], EMPTY_STRING)
    assert helpers.get_file_timestamps(base_input + timestamp) == (True, [timestamp], base_input)
    assert helpers.get_file_timestamps(base_input + timestamp + base_input + timestamp) \
        == (True, [timestamp, timestamp], base_input * 2)

    other_input = base_input[::-1]
    other_timestamp = datetime_to_string(datetime + timedelta(10))
    assert helpers.get_file_timestamps(base_input + other_timestamp + other_input + timestamp) \
        == (True, [other_timestamp, timestamp], base_input + other_input)

@pytest.mark.parametrize("time_units, expected_result", [
    (None, EMPTY_STRING),
    ([], EMPTY_STRING),
    (['non_exist_time_unit'], EMPTY_STRING),
    (['non_exist_time_unit', 'day'], '--day '),
    (['hour', 'non_exist_time_unit', 'day'], '--hour --day '),
    (['hour', 'hour'], '--hour '),
])
def test_time_units_to_command_string(time_units, expected_result):
    assert helpers.time_units_to_command_string(time_units) == expected_result
