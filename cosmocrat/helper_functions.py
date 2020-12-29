import os
import re
import sys
import subprocess
import cosmocrat.definitions as definitions

from osmeterium.run_command import run_command
from cosmocrat.definitions import log, Subprocess_Tool

def log_and_exit(exception_message, exit_code):
    log.error(exception_message)
    sys.exit(exit_code)

def subprocess_error_handler_wrapper(subprocess_name, already_raised_exit_code=None):
    exit_code_value = 'general_error'
    logged_message_head = 'The subprocess'
    if subprocess_name in Subprocess_Tool._member_names_:
        exit_code_value = f'{subprocess_name}_error'
        logged_message_head = subprocess_name
    def error_handler(exit_code=already_raised_exit_code):
        log.error(fr'{logged_message_head} raised an error: {exit_code}')
        sys.exit(definitions.EXIT_CODES[exit_code_value])
    return error_handler

def run_command_wrapper(command, subprocess_name=''):
    run_command(command,
                log.info,
                log.info,
                subprocess_error_handler_wrapper(subprocess_name),
                (lambda: log.info('subprocess finished successfully.')))

def subprocess_get_stdout_output(args, subprocess_name=''):
    completed_process = subprocess.run(args=args,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        universal_newlines=True)
    return_code = completed_process.returncode                   
    if return_code is not 0:
        subprocess_error_handler_wrapper(subprocess_name,
                                        already_raised_exit_code=return_code)()
    output = completed_process.stdout
    return output.strip()

def get_compression_method(compression, default_format=''):
    compression_type = 'none'
    compression_format = default_format
    if compression:
        compression_type = 'gzip'
        compression_format += '.gz'
    return (compression_type, compression_format)

def deconstruct_file_path(string):
    (_, format, string) = get_file_format(string)
    (_, dir, string) = get_file_dir(string)
    (_, timestamps, string) = get_file_timestamps(string)
    if len(timestamps) is 1:
        timestamps = timestamps[0]
    name = remove_dots_from_edges_of_string(string)
    return (dir, name, timestamps, format)

def get_file_format(input):
    format = ''
    successful = False
    rest = input
    for format_value in definitions.FORMATS_MAP.values():
        index = input.find(f'.{format_value}')
        if index is not -1 and len(format) < len(format_value):
            format = format_value
            successful = True
    if successful:
        rest = input[:input.rfind(format)]
    return (successful, format, rest)

def get_file_dir(input):
    index = input.rfind('/')
    if index is -1:
        return (False, None, input)
    path = input[:index]
    rest = input[index + 1:]
    return (True, path, rest)

def get_file_timestamps(input):
    timestamps = []
    success = False
    for match in re.finditer(definitions.TIMESTAMP_REGEX, input):
        success = True
        timestamp = match.group(0)
        timestamps.append(timestamp)
    rest = remove_datetime_from_string(input)
    return (success, timestamps, rest)

def remove_dots_from_edges_of_string(input):
    output = re.sub(r'(^[.])|([.]$)', '', input)
    if input is not output:
        output = remove_dots_from_edges_of_string(output)
    return output

def remove_datetime_from_string(input):
    return re.sub(definitions.TIMESTAMP_REGEX, '', input)
