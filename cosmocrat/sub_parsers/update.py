import cosmocrat.definitions as definitions
import cosmocrat.argument_parser.validation.action_validators as validators

from cosmocrat.helper_functions import safe_copy
from cosmocrat.osm_tools.osmupdate import get_changes_from_file, get_changes_from_timestamp

def register_parser(sub_parser):
    parser_update = sub_parser.add_parser('update', help='Get global osm changes from a given file or timestamp')
    exgroup = parser_update.add_argument_group(title='one or the other')
    group = exgroup.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--input_path', action=validators.validate_input_path)
    group.add_argument('-t', '--timestamp', action=validators.validate_timestamp)
    parser_update.add_argument('-s', '--source', action=validators.validate_url, default=definitions.REPLICATION_SERVER_BASE_URL)
    parser_update.add_argument('-l','--limit', nargs='+', action=validators.validate_time_units_limit, default=definitions.TIME_UNITS_IN_USE)
    parser_update.add_argument('output_path', action=validators.validate_output_path)
    fm=definitions.FORMATS_MAP
    parser_update.add_argument('-f', '--output_format',
                                choices=[fm['OSC'], fm['OSC_GZ'], fm['OSC_BZ2']], default=fm['OSC'])
    parser_update.set_defaults(func=lambda args: update(
                                args.input_path,
                                args.timestamp,
                                args.source,
                                args.limit,
                                args.output_path,
                                args.output_format
    ))

def update(input_path, timestamp, source, limited_time_units, output_path, output_format):
    if input_path:
        get_function=get_changes_from_file
        get_input=input_path
    elif timestamp:
        get_function=get_changes_from_timestamp
        get_input=timestamp

    changes_path = get_function(get_input,
                    changes_format=output_format,
                    source=source,
                    limited_time_units=limited_time_units)

    safe_copy(changes_path, output_path)