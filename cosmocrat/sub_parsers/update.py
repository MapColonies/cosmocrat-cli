import shutil
import cosmocrat.definitions as definitions

from cosmocrat.action_validators import validate_input_path, validate_output_path, validate_timestamp
from cosmocrat.osm_tools.osmupdate import get_changes_from_file, get_changes_from_timestamp

def register_parser(sub_parser):
    parser_update = sub_parser.add_parser('update', help='Get global osm changes from a given file or timestamp')
    exgroup = parser_update.add_argument_group(title='one or the other')
    group = exgroup.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--input_path', action=validate_input_path)
    group.add_argument('-t', '--timestamp', action=validate_timestamp)
    parser_update.add_argument('output_path', action=validate_output_path)
    parser_update.add_argument('-f', '--output_format', choices=['osc', 'osc.gz', 'osc.bz2'], default='osc')
    parser_update.set_defaults(func=lambda args: update(
                                args.input_path,
                                args.timestamp,
                                args.output_path,
                                args.output_format
    ))

def update(input_path, timestamp, output_path, output_format):
    if input_path:
        changes_path = get_changes_from_file(input_path=input_path,
                                changes_format=output_format)
    elif timestamp:
        changes_path = get_changes_from_timestamp(input_timestamp=timestamp,
                                changes_format=output_format)
    shutil.copy(changes_path, output_path)