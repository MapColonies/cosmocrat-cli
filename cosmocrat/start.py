import os
import argparse

from cosmocrat.custom_argument_parser import CustomArgumentParser
from cosmocrat.helper_functions import log_and_exit

import cosmocrat.definitions as definitions
import cosmocrat.sub_parsers.apply as apply
import cosmocrat.sub_parsers.clip as clip
import cosmocrat.sub_parsers.delta as delta
import cosmocrat.sub_parsers.drop as drop
import cosmocrat.sub_parsers.update as update

def create_parser():
    parser = CustomArgumentParser(prog='cosmocrat')
    sub_parsers = parser.add_subparsers(dest='command', metavar='<command>')
    apply.register_parser(sub_parsers)
    clip.register_parser(sub_parsers)
    delta.register_parser(sub_parsers)
    drop.register_parser(sub_parsers)
    update.register_parser(sub_parsers)
    return parser

def parse_args(parser):
    try:
        return parser.parse_args()
    except argparse.ArgumentTypeError as arg_type_exc:
        log_and_exit(exception_message=arg_type_exc.args[0],
                    exit_code=definitions.EXIT_CODES['invalid_argument'])
    except argparse.ArgumentError as arg_exc:
        exc_message = f'{arg_exc.argument_name}: {arg_exc.message}'
        exit_code = definitions.EXIT_CODES['invalid_argument']
        if arg_exc.argument.dest is 'command':
            parser.print_help()
            exit_code = definitions.EXIT_CODES['not_found']
        log_and_exit(exception_message=exc_message,
                    exit_code=exit_code)
    except:
        exit(definitions.EXIT_CODES['general_error'])

def prepare_env():
    os.makedirs(definitions.RESULTS_PATH, exist_ok=True)
    os.makedirs(definitions.DELTAS_PATH, exist_ok=True)
    os.makedirs(definitions.OSMCHANGES_PATH, exist_ok=True)
    for compression_format in definitions.COMPRESSION_METHOD_MAP:
        os.makedirs(os.path.join(definitions.OSMCHANGES_PATH, compression_format), exist_ok=True)

def main():
    prepare_env()
    parser = create_parser()
    args = parse_args(parser)
    args.func(args)
    exit(definitions.EXIT_CODES['success'])

if __name__ == '__main__':
    main()