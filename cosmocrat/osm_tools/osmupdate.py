import os
import cosmocrat.definitions as definitions

from uuid import uuid4
from cosmocrat.helper_functions import run_command_wrapper
from cosmocrat.osm_tools.osmconvert import get_osm_file_timestamp

SUBPROCESS_NAME='osmupdate'

def time_units_to_command_string(time_units):
    result = ''
    for time_unit in time_units:
        if time_unit not in definitions.Time_Unit._member_names_:
            continue
        result += f'--{time_unit} '
    return result

def get_changes_from_timestamp(input_timestamp, changes_format, source, limited_time_units):
    temp_output_name = f'{uuid4()}.{changes_format}'
    output_path = os.path.join(definitions.OSMCHANGES_PATH, changes_format, temp_output_name)

    run_command_wrapper(f'{definitions.OSMUPDATE_PATH} \
                    {input_timestamp} \
                    {output_path} \
                    {time_units_to_command_string(limited_time_units)} \
                    --base-url={source} \
                    --tempfiles={definitions.OSMUPDATE_CACHE_PATH} \
                    --keep-tempfiles \
                    --trust-tempfiles \
                    -v',
                    subprocess_name=SUBPROCESS_NAME)

    output_timestamp = get_osm_file_timestamp(output_path)
    output_name = f'{input_timestamp}.{output_timestamp}.{changes_format}'
    new_output_path = os.path.join(definitions.OSMCHANGES_PATH, changes_format, output_name)
    os.rename(output_path, new_output_path)
    return new_output_path

def get_changes_from_file(input_path, changes_format, source, limited_time_units):
    temp_output_name = f'{uuid4()}.{changes_format}'
    output_path = os.path.join(definitions.OSMCHANGES_PATH, changes_format, temp_output_name)

    run_command_wrapper(f'{definitions.OSMUPDATE_PATH} \
                    {input_path} \
                    {output_path} \
                    {time_units_to_command_string(limited_time_units)} \
                    --base-url={source} \
                    --tempfiles={definitions.OSMUPDATE_CACHE_PATH} \
                    --keep-tempfiles \
                    --trust-tempfiles \
                    -v',
                    subprocess_name=SUBPROCESS_NAME)

    input_timestamp = get_osm_file_timestamp(input_path)
    output_timestamp = get_osm_file_timestamp(output_path)
    output_name = f'{input_timestamp}.{output_timestamp}.{changes_format}'
    new_output_path = os.path.join(definitions.OSMCHANGES_PATH, changes_format, output_name)
    os.rename(output_path, new_output_path)
    return new_output_path