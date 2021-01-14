import pytest
import unittest.mock as mock
import os
import cosmocrat.definitions as definitions

from cosmocrat.osm_tools import osmosis
from tests.definitions import EMPTY_STRING, FULL_FILE_PATH, FILE_PATH, FILE_NAME, FILE_FORMAT, FAKE_MULTI_PURPOSE
from tests.helpers.helpers import ArgumentWildcard

SUBPROCESS_NAME=osmosis.SUBPROCESS_NAME
OSMOSIS_MODULE_PATH='cosmocrat.osm_tools.osmosis'

fake = FAKE_MULTI_PURPOSE

@pytest.mark.osm_tools
@mock.patch(f'{OSMOSIS_MODULE_PATH}.run_command_wrapper')
class TestOsmupdate():
    @pytest.mark.parametrize("exist_ok, file_exists", [
        (True, True),
        (True, False),
        (False, True),
        (False, False)
    ])
    @mock.patch(f'{OSMOSIS_MODULE_PATH}.deconstruct_file_path',
        return_value=(fake, fake, fake, fake))
    def test_clip_polygon(self,
        mock_deconstruct,
        mock_run_command_wrapper,
        exist_ok,
        file_exists):
        input_path = fake
        polygon_path = fake
        input_timestamp = fake
        base_output_path = fake

        _, some_name, _, _ = mock_deconstruct.return_value
        output_format = definitions.FORMATS_MAP['OSM_PBF']
        output_name = f'{some_name}.{some_name}.{input_timestamp}.{output_format}'
        output_path = os.path.join(base_output_path, output_name)

        with mock.patch('os.path.isfile', return_value=file_exists) as mock_isfile:
            res = osmosis.clip_polygon(input_path, polygon_path, input_timestamp, base_output_path, exist_ok)

        if mock_run_command_wrapper.called:
            _, kwargs = mock_run_command_wrapper.call_args
            command = kwargs.get('command')

            # command starts with
            assert command.startswith(definitions.OSMOSIS_PATH)

            # arguments in command
            expected_in_command = [f'--read-pbf-fast file={input_path}',
                                    f'--bounding-polygon file={polygon_path}',
                                    'completeWays=true completeRelations=true',
                                    f'--write-pbf file={output_path}']
            for expected in expected_in_command:
                assert expected in command

        # mock functions
        mock_isfile.assert_called_with(output_path) if exist_ok else mock_isfile.assert_not_called()
        mock_run_command_wrapper.assert_not_called() if exist_ok and file_exists \
            else mock_run_command_wrapper.assert_called_with(
                command=ArgumentWildcard(),
                subprocess_name=SUBPROCESS_NAME)

        # result
        assert res == output_path
