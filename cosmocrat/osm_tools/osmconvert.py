import os
import cosmocrat.definitions as definitions

from uuid import uuid4
from cosmocrat.helper_functions import subprocess_get_stdout_output, run_command_wrapper, deconstruct_file_path

SUBPROCESS_NAME='osmconvert'

def get_osm_file_timestamp(input_path):
    command = [definitions.OSMCONVERT_PATH, '--out-timestamp', input_path, '--verbose']
    return subprocess_get_stdout_output(command, SUBPROCESS_NAME)

def set_osm_file_timestamp(input_path, new_timestamp):
    (dir, name, _, input_format) = deconstruct_file_path(input_path)
    temp_path = os.path.join(dir, f'{str(uuid4())}.{input_format}')
    run_command_wrapper(f'{definitions.OSMCONVERT_PATH} \
                    {input_path} \
                    --timestamp={new_timestamp} \
                    -o={temp_path} \
                    --verbose',
                    subprocess_name=SUBPROCESS_NAME)
    output_name = f'{name}.{new_timestamp}.{input_format}'
    output_path = os.path.join(dir, output_name)
    os.rename(temp_path, output_path)
    return output_path

def drop_author(input_path, output_path=None):
    (input_dir, _, _, input_format) = deconstruct_file_path(input_path)
    output_not_given = False
    if output_path is None:
        output_not_given = True
        output_path = os.path.join(input_dir, f'{str(uuid4())}.{input_format}')
    run_command_wrapper(f'{definitions.OSMCONVERT_PATH} \
                    --drop-author \
                    {input_path} \
                    -o={output_path} \
                    --verbose', 
                    subprocess_name=SUBPROCESS_NAME)
    if output_not_given:
        os.rename(output_path, input_path)
    