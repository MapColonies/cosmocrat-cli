import pytest
import unittest
import unittest.mock as mock
import argparse

from cosmocrat.argument_parser.custom_argument_parser import CustomArgumentParser
from cosmocrat.start import argparse_parse_args, create_parser
from tests.helpers.helpers import ARGPARSE_ERROR_MAP

@pytest.fixture
def custom_argument_parser():
    '''Returns an empty custom_argument_parser'''
    return CustomArgumentParser()

@mock.patch.object(CustomArgumentParser, '_get_action_from_name', autospec=True)
@mock.patch('argparse.ArgumentParser.error')
@mock.patch('sys.exc_info')
class TestCustomArgumentParserError():
    @mock.patch('argparse._get_action_name')
    def test_error_raised_with_argument(
        self,
        mock_argparse_get_action_name,
        mock_exc_info,
        mock_argparser_base_error,
        mock_get_action,
        custom_argument_parser):
        mock_argparse_get_action_name.return_value = 'action_name'
        mock_exc_info.return_value = \
            [None, argparse.ArgumentError(argument='exc', message='msg')]

        with pytest.raises(argparse.ArgumentError):
            custom_argument_parser.error(message='')
        mock_get_action.assert_called_with(custom_argument_parser, 'action_name')
        mock_argparser_base_error.assert_not_called()

    def test_error_raised_with_no_argument(
        self,
        mock_exc_info,
        mock_argparser_base_error,
        mock_get_action,
        custom_argument_parser):
        mock_exc_info.return_value = \
            [None, argparse.ArgumentError(argument=None, message='msg')]

        with pytest.raises(argparse.ArgumentError):
            custom_argument_parser.error(message='')
        mock_get_action.assert_called_with(custom_argument_parser, None)
        mock_argparser_base_error.assert_not_called()

    def test_error_raised_from_super(
        self,
        mock_exc_info,
        mock_argparser_base_error,
        mock_get_action,
        custom_argument_parser):
        mock_exc_info.return_value = [None, None]

        custom_argument_parser.error('some_message')
        mock_get_action.assert_not_called()
        mock_argparser_base_error.assert_called_with('some_message')

@pytest.mark.parametrize("name, option_strings, metavar, dest, result_should_be_none", [
    (None, None, None, None, True),
    ('', None, None, None, True),
    ('', 'name', '-n/--name', 'name', True),
    ('-n/--name', ['-n', '--name'], None, None, False),
    ('dest', None, None, 'dest', False),
    ('metavar', None, 'metavar', 'dest', False),
    ('dest', None, 'metavar', 'dest', False)
])
def test_get_action_from_name_v2(
    custom_argument_parser,
    name,
    option_strings,
    metavar,
    dest,
    result_should_be_none):
    action = mock.Mock(option_strings=option_strings, metavar=metavar, dest=dest)
    setattr(custom_argument_parser, '_actions', [action])

    result = custom_argument_parser._get_action_from_name(name=name)
    assert result is None if result_should_be_none else action

@pytest.mark.parametrize("error_type, should_call_help", [
    ('general', False),
    ('argument_type', False),
    ('argument', False),
    ('command', True)
])
@mock.patch.object(argparse.ArgumentParser, 'print_help')
@mock.patch('cosmocrat.start.log_and_exit')
@mock.patch.object(argparse.ArgumentParser, 'parse_args')
def test_argparse_parse_args_error(
    mock_parse_args,
    mock_log_and_exit,
    mock_print_help,
    custom_argument_parser,
    error_type,
    should_call_help):
    expected_map = ARGPARSE_ERROR_MAP.get(error_type)

    mock_parse_args.side_effect = expected_map['exception'](
        *expected_map['exception_args'],
        **expected_map['exception_kwargs'])

    if error_type is 'command':
        mock_dest = mock.Mock(dest='command')
        setattr(mock_parse_args.side_effect, 'argument', mock_dest)

    argparse_parse_args(custom_argument_parser)

    mock_parse_args.assert_called()
    mock_print_help.assert_called() if should_call_help else mock_print_help.assert_not_called()
    mock_log_and_exit.assert_called_with(
        exception_message=mock.ANY,
        exit_code=expected_map['exit_code'])

def test_create_parser():
    assert type(create_parser()) is CustomArgumentParser