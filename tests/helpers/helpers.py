import cosmocrat.definitions as definitions
import unittest.mock as mock
import argparse

from datetime import datetime, timezone

def get_current_datetime():
    return datetime.now(tz=timezone.utc)

def datetime_to_string(datetime):
    return datetime.strftime(r'%Y-%m-%dT%H:%M:%SZ')

class Expected_In_Arg():
    def __init__(self, **kwargs):
        self.expressions = kwargs.get('expressions', [])
        self.head = kwargs.get('head')

    def __eq__(self, argument):
        if self.head and not argument.startswith(self.head):
            return False
        for expression in self.expressions:
            if expression not in argument:
                return False
        return True

ARGPARSE_ERROR_MAP = {
    'general': {
        'exit_code': definitions.EXIT_CODES['general_error'],
        'exception': BaseException,
        'exception_args': (),
        'exception_kwargs': {}
    },
    'argument_type': {
        'exit_code': definitions.EXIT_CODES['invalid_argument'],
        'exception': argparse.ArgumentTypeError,
        'exception_args': ('arg'),
        'exception_kwargs': {}
    },
    'argument': {
        'exit_code': definitions.EXIT_CODES['invalid_argument'],
        'exception': argparse.ArgumentError,
        'exception_args': (),
        'exception_kwargs': {
            'argument': mock.Mock(option_strings=None, metavar=None, dest=None),
            'message': 'msg'
        }
    },
    'command': {
        'exit_code': definitions.EXIT_CODES['not_found'],
        'exception': argparse.ArgumentError,
        'exception_args': (),
        'exception_kwargs': {
            'argument': mock.Mock(option_strings=None, metavar=None, dest='command'),
            'message': 'msg'
        }
    }
}