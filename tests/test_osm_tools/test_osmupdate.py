import pytest
import unittest.mock as mock
import os
import cosmocrat.definitions as definitions

from cosmocrat.osm_tools import osmupdate
from tests.helpers.helpers import ArgumentWildcard, get_current_datetime, datetime_to_string
from tests.definitions import EMPTY_STRING, FILE_FORMAT, FAKE_MULTI_PURPOSE

SUBPROCESS_NAME=osmupdate.SUBPROCESS_NAME
OSMUPDATE_MODULE_PATH='cosmocrat.osm_tools.osmupdate'

@pytest.mark.osm_tools
@mock.patch(f'{OSMUPDATE_MODULE_PATH}.uuid4', return_value='uuid')
@mock.patch(f'{OSMUPDATE_MODULE_PATH}.get_osm_file_timestamp', return_value=FAKE_MULTI_PURPOSE)
@mock.patch(f'{OSMUPDATE_MODULE_PATH}.run_command_wrapper')
class TestOsmupdate():
    @pytest.mark.parametrize("get_function", [
        (osmupdate.get_changes_from_timestamp),
        (osmupdate.get_changes_from_file)
    ])
    def test_get_changes(self,
        mock_run_command_wrapper,
        mock_get_osm_file_timestamp,
        mock_uuid4,
        get_function):
        input_path_or_timestamp = FAKE_MULTI_PURPOSE
        changes_format = FILE_FORMAT
        source = EMPTY_STRING
        limited_time_units = None

        inner_output_path = os.path.join(definitions.OSMCHANGES_PATH, changes_format,
                            f'{mock_uuid4.return_value}.{changes_format}')
        output_name = f'{input_path_or_timestamp}.{mock_get_osm_file_timestamp.return_value}.{changes_format}'
        new_output_path = os.path.join(definitions.OSMCHANGES_PATH, changes_format, output_name)

        with mock.patch('os.rename') as mock_rename:
            res = get_function(input_path_or_timestamp,
                                changes_format,
                                source,
                                limited_time_units)

        _, kwargs = mock_run_command_wrapper.call_args
        command = kwargs.get('command')

        # command starts with
        assert command.startswith(definitions.OSMUPDATE_PATH)

        # arguments in command
        expected_in_command = [input_path_or_timestamp,
                                inner_output_path,
                                f'--base-url={source}',
                                f'--tempfiles={definitions.OSMUPDATE_CACHE_PATH}',
                                '--keep-tempfiles',
                                '--trust-tempfiles']
        for expected in expected_in_command:
            assert expected in command

        # arguments in wrapper
        mock_run_command_wrapper.assert_called_with(
            command=ArgumentWildcard(),
            subprocess_name=SUBPROCESS_NAME)

        # mocked functions
        mock_rename.assert_called_with(inner_output_path, new_output_path)

        files_to_get_timestamp_from = [inner_output_path, input_path_or_timestamp]
        for index, call in enumerate(mock_get_osm_file_timestamp.call_args_list):
            _, kwargs = call
            file_path = kwargs.get('input_path')
            assert file_path == files_to_get_timestamp_from[index]

        # result
        assert res == new_output_path