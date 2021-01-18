import pytest
import unittest.mock as mock
import os
import cosmocrat.definitions as definitions

from cosmocrat.osm_tools import osmconvert
from tests.definitions import EMPTY_STRING, FILE_PATH, FILE_NAME, FILE_FORMAT, FAKE_MULTI_PURPOSE
from tests.helpers.helpers import Expected_In_Arg

SUBPROCESS_NAME=osmconvert.SUBPROCESS_NAME
OSMCONVERT_MODULE_PATH='cosmocrat.osm_tools.osmconvert'

@pytest.mark.osm_tools
@mock.patch('cosmocrat.definitions.OSMCONVERT_PATH', FAKE_MULTI_PURPOSE)
class TestOsmconvert():
    @mock.patch(f'{OSMCONVERT_MODULE_PATH}.subprocess_get_stdout_output')
    def test_get_osm_file_timestamp(self, mock_get_stdout):
        input_path = FAKE_MULTI_PURPOSE

        result = osmconvert.get_osm_file_timestamp(input_path)

        # arguments in command
        mock_get_stdout.assert_called_with(
            args=[definitions.OSMCONVERT_PATH,
            '--out-timestamp',
            input_path,
            mock.ANY],
            subprocess_name=SUBPROCESS_NAME)

        # result
        assert result == mock_get_stdout.return_value

    @mock.patch(f'{OSMCONVERT_MODULE_PATH}.run_command_wrapper')
    def test_set_osm_file_timestamp(self, mock_run_command_wrapper):
        input_path = FAKE_MULTI_PURPOSE
        timestamp = FAKE_MULTI_PURPOSE[::-1]

        with mock.patch('os.rename') as mock_rename, \
        mock.patch(f'{OSMCONVERT_MODULE_PATH}.uuid4', return_value='uuid') as mock_uuid4, \
        mock.patch(f'{OSMCONVERT_MODULE_PATH}.deconstruct_file_path',
        return_value=(FILE_PATH, FILE_NAME, EMPTY_STRING, FILE_FORMAT)):
            res = osmconvert.set_osm_file_timestamp(input_path, timestamp)

        temp_file_name = os.path.join(FILE_PATH,
            f'{mock_uuid4.return_value}.{FILE_FORMAT}')

        _, kwargs = mock_run_command_wrapper.call_args
        command = kwargs.get('command')

        # arguments in command
        expected_in_command = [input_path, f'--timestamp={timestamp}', f'-o={temp_file_name}']

        # arguments in wrapper
        mock_run_command_wrapper.assert_called_with(
            command=Expected_In_Arg(expressions=expected_in_command, head=definitions.OSMCONVERT_PATH),
            subprocess_name=SUBPROCESS_NAME)

        # mocked functions
        mock_rename.assert_called_with(mock.ANY, res)

        # result
        assert res == os.path.join(FILE_PATH, f'{FILE_NAME}.{timestamp}.{FILE_FORMAT}')

    @mock.patch(f'{OSMCONVERT_MODULE_PATH}.run_command_wrapper')
    def test_drop_author_without_output(self, mock_run_command_wrapper):
        input_path = FAKE_MULTI_PURPOSE

        with mock.patch('os.rename') as mock_rename, \
        mock.patch(f'{OSMCONVERT_MODULE_PATH}.uuid4', return_value='uuid') as mock_uuid4, \
        mock.patch(f'{OSMCONVERT_MODULE_PATH}.deconstruct_file_path',
        return_value=(FILE_PATH, FILE_NAME, EMPTY_STRING, FILE_FORMAT)):
            res = osmconvert.drop_author(input_path)

        output_path=os.path.join(FILE_PATH, f'{mock_uuid4.return_value}.{FILE_FORMAT}')

        _, kwargs = mock_run_command_wrapper.call_args
        command = kwargs.get('command')

        # arguments in command
        expected_in_command = ['--drop-author', input_path, f'-o={output_path}']

        # arguments in wrapper
        mock_run_command_wrapper.assert_called_with(
            command=Expected_In_Arg(expression=expected_in_command, head=definitions.OSMCONVERT_PATH),
            subprocess_name=SUBPROCESS_NAME)

        # mocked functions
        mock_uuid4.assert_called_once()
        mock_rename.assert_called_with(output_path, res)

        # result
        assert res == input_path

    @mock.patch(f'{OSMCONVERT_MODULE_PATH}.run_command_wrapper')
    def test_drop_author_with_output(self, mock_run_command_wrapper):
        input_path = FAKE_MULTI_PURPOSE
        output_path= FAKE_MULTI_PURPOSE[::-1]

        with mock.patch('os.rename') as mock_rename, \
        mock.patch(f'{OSMCONVERT_MODULE_PATH}.uuid4', return_value='uuid') as mock_uuid4, \
        mock.patch(f'{OSMCONVERT_MODULE_PATH}.deconstruct_file_path',
        return_value=(FILE_PATH, FILE_NAME, EMPTY_STRING, FILE_FORMAT)):
            res = osmconvert.drop_author(input_path, output_path)

        _, kwargs = mock_run_command_wrapper.call_args
        command = kwargs.get('command')

        # arguments in command
        expected_in_command = ['--drop-author', input_path, f'-o={output_path}']

        # arguments in wrapper
        mock_run_command_wrapper.assert_called_with(
            command=Expected_In_Arg(expressions=expected_in_command, head=definitions.OSMCONVERT_PATH),
            subprocess_name=SUBPROCESS_NAME)

        # mocked functions
        mock_uuid4.assert_not_called()
        mock_rename.assert_not_called()

        # result
        assert res == output_path