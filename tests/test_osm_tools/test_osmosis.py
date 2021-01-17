import pytest
import unittest
import unittest.mock as mock
import os
import cosmocrat.definitions as definitions

from cosmocrat.osm_tools import osmosis
from tests.definitions import FILE_FORMAT, FAKE_MULTI_PURPOSE
from tests.helpers.helpers import Expected_In_Arg

SUBPROCESS_NAME=osmosis.SUBPROCESS_NAME
OSMOSIS_MODULE_PATH='cosmocrat.osm_tools.osmosis'
fake = FAKE_MULTI_PURPOSE

@pytest.mark.osm_tools
@mock.patch('cosmocrat.definitions.OSMOSIS_PATH', fake)
@mock.patch.dict('cosmocrat.definitions.FORMATS_MAP', {'OSM_PBF': fake, 'OSC': fake})
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
        input_path, polygon_path, input_timestamp, base_output_path = (fake,) * 4

        _, some_name, _, _ = mock_deconstruct.return_value
        output_format = definitions.FORMATS_MAP['OSM_PBF']
        output_name = f'{some_name}.{some_name}.{input_timestamp}.{output_format}'
        output_path = os.path.join(base_output_path, output_name)

        with mock.patch('os.path.isfile', return_value=file_exists) as mock_isfile:
            res = osmosis.clip_polygon(input_path, polygon_path, input_timestamp, base_output_path, exist_ok)

        if mock_run_command_wrapper.called:
            _, kwargs = mock_run_command_wrapper.call_args
            command = kwargs.get('command')

            # arguments in command
            expected_in_command = [f'--read-pbf-fast file={input_path}',
                                    f'--bounding-polygon file={polygon_path}',
                                    'completeWays=true completeRelations=true',
                                    f'--write-pbf file={output_path}']

        # mock functions
        mock_isfile.assert_called_with(output_path) if exist_ok else mock_isfile.assert_not_called()
        mock_run_command_wrapper.assert_not_called() if exist_ok and file_exists \
        else mock_run_command_wrapper.assert_called_with(
            command=Expected_In_Arg(expressions=expected_in_command, head=definitions.OSMOSIS_PATH),
            subprocess_name=SUBPROCESS_NAME)

        # result
        assert res == output_path

    @mock.patch.dict('cosmocrat.definitions.COMPRESSION_METHOD_MAP', { fake: fake })
    @mock.patch(f'{OSMOSIS_MODULE_PATH}.deconstruct_file_path',
        return_value=(fake, fake, fake, fake))
    def test_apply_changes_by_polygon(self,
        mock_deconstruct,
        mock_run_command_wrapper):
        base_output_path, input_path, change_path, polygon_path = (fake,) * 4
        _, input_name, changes_timestamps, changes_format = mock_deconstruct.return_value
        compression_type = definitions.COMPRESSION_METHOD_MAP[changes_format]
        output_format = definitions.FORMATS_MAP['OSM_PBF']
        output_path = os.path.join(base_output_path, f'{input_name}.{changes_timestamps}.{output_format}')
        res = osmosis.apply_changes_by_polygon(base_output_path, input_path, change_path, polygon_path)

        _, kwargs = mock_run_command_wrapper.call_args
        command = kwargs.get('command')

        # arguments in command
        expected_in_command = [f'--read-pbf-fast file={input_path}',
                                f'--read-xml-change compressionMethod={compression_type} file={change_path}',
                                '--apply-change',
                                f'--bounding-polygon file={polygon_path}',
                                f'--write-pbf file={output_path}']

        # arguments in wrapper
        mock_run_command_wrapper.assert_called_with(
            command=Expected_In_Arg(expressions=expected_in_command, head=definitions.OSMOSIS_PATH),
            subprocess_name=SUBPROCESS_NAME)

        # mocked functions
        assert mock_deconstruct.call_count == 2

        # result
        assert res == output_path


    @pytest.mark.parametrize("compression_type", [
        ('gzip'),
        ('none')
    ])
    @mock.patch(f'{OSMOSIS_MODULE_PATH}.get_compression_method')
    def test_create_delta(self,
    mock_get_compression,
    mock_run_command_wrapper,
    compression_type):
        delta_path, delta_name, first_input_pbf_path, first_input_pbf_path, second_input_pbf_path, should_compress, output_format = (fake,) * 7
        output_name = f'{delta_name}.{output_format}'
        output_path = os.path.join(delta_path, output_name)
        mock_get_compression.return_value = (compression_type, output_format)

        res = osmosis.create_delta(delta_path,
                                    delta_name,
                                    first_input_pbf_path,
                                    second_input_pbf_path,
                                    should_compress)

        _, kwargs = mock_run_command_wrapper.call_args
        command = kwargs.get('command')

        # arguments in command
        expected_in_command = [f'--read-pbf-fast file={first_input_pbf_path}',
                                f'--read-pbf-fast file={second_input_pbf_path}',
                                '--derive-change',
                                f'--write-xml-change compressionMethod={compression_type} file={output_path}']

        # arguments in wrapper
        mock_run_command_wrapper.assert_called_with(
            command=Expected_In_Arg(expressions=expected_in_command, head=definitions.OSMOSIS_PATH),
            subprocess_name=SUBPROCESS_NAME)

        # mocked functions
        mock_get_compression.assert_called_with(compression=should_compress,
                                base_format=definitions.FORMATS_MAP['OSC'])

        # result
        assert res == output_path