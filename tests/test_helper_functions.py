import pytest
import unittest.mock as mock
from os.path import join

import cosmocrat.definitions as definitions
import cosmocrat.helper_functions as helpers
from tests.helpers.helpers import get_current_datetime, datetime_to_string
from random import randrange
from datetime import datetime, timedelta
from tests.definitions import EMPTY_STRING, FILE_PATH, FILE_NAME, FILE_FORMAT, FAKE_MULTI_PURPOSE, FULL_FILE_PATH

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

subprocess_output_dict = {
    'no_error': {'returncode': 0, 'stdout': f'\n{FAKE_MULTI_PURPOSE}\n'},
    'error': {'returncode': 1, 'stdout': 'some_error'}
}

@mock.patch('cosmocrat.helper_functions.subprocess_error_handler_wrapper')
@mock.patch('cosmocrat.helper_functions.subprocess.run')
def test_subprocess_get_stdout_output_no_error(mock_subprocess_run, mock_subprocess_error_handler):
    mock_subprocess_run.return_value = mock.Mock(**subprocess_output_dict.get('no_error'))
    stdout_output = helpers.subprocess_get_stdout_output(None)
    mock_subprocess_error_handler.assert_not_called()
    assert stdout_output == FAKE_MULTI_PURPOSE

@mock.patch('cosmocrat.helper_functions.subprocess_error_handler_wrapper')
@mock.patch('cosmocrat.helper_functions.subprocess.run')
def test_subprocess_get_stdout_output_raises_error(mock_subprocess_run, subprocess_error_handler_wrapper):
    mock_subprocess_run.return_value = mock.Mock(**subprocess_output_dict.get('error'))
    helpers.subprocess_get_stdout_output(None)
    mock_subprocess_run.assert_called()
    subprocess_error_handler_wrapper.assert_called()

@pytest.mark.parametrize("subprocess_name, error_code, logged_message_head", [
    (EMPTY_STRING, 1, 'The subprocess'),
    (FAKE_MULTI_PURPOSE, 1, 'The subprocess'),
    ('osmosis', definitions.EXIT_CODES.get('osmosis_error'), 'osmosis')
])
def test_map_subprocess_name_to_error(subprocess_name, error_code, logged_message_head):
    assert helpers.map_subprocess_name_to_error(subprocess_name) == (error_code, logged_message_head)

@pytest.mark.parametrize("subprocess_name, error_code, logged_message_head, already_raised_exit_code", [
    (EMPTY_STRING, 1, 'The subprocess', None),
    (FAKE_MULTI_PURPOSE, 1, 'The subprocess', None),
    ('osmosis', definitions.EXIT_CODES.get('osmosis_error'), 'osmosis', None),
    ('osmconvert', 1, 'osmconvert', definitions.EXIT_CODES.get('osmconvert_error'))
])
@mock.patch('cosmocrat.helper_functions.log.error')
@mock.patch('cosmocrat.helper_functions.sys.exit')
@mock.patch('cosmocrat.helper_functions.map_subprocess_name_to_error')
def test_subprocess_error_handler_wrapper(
        mock_subprocess_error,
        sys_exit,
        log_error,
        subprocess_name,
        error_code,
        logged_message_head,
        already_raised_exit_code):
    mock_subprocess_error.return_value = (error_code, logged_message_head)
    error_handler_func = helpers.subprocess_error_handler_wrapper(subprocess_name)
    error_handler_func(exit_code=already_raised_exit_code)
    log_error.assert_called_with(f'{logged_message_head} raised an error: {already_raised_exit_code}')
    sys_exit.assert_called_with(error_code)

def test_safe_copy():
    import shutil
    test_func = lambda: helpers.safe_copy(EMPTY_STRING, EMPTY_STRING)

    with mock.patch('shutil.copy', side_effect=shutil.SameFileError):
        assert test_func() is None

    with mock.patch('shutil.copy', side_effect=shutil.Error), pytest.raises(shutil.Error):
        test_func()

@mock.patch('sys.exit')
@mock.patch('cosmocrat.helper_functions.log.error')
def test_log_and_exit(mock_log_error, mock_sys_exit):
    helpers.log_and_exit(exception_message=EMPTY_STRING, exit_code=EMPTY_STRING)
    mock_log_error.assert_called_with(EMPTY_STRING)
    mock_sys_exit.assert_called_with(EMPTY_STRING)
