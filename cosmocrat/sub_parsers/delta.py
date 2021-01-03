import cosmocrat.definitions as definitions

from cosmocrat.action_validators import validate_input_path, validate_output_path
from cosmocrat.osm_tools.osmosis import create_delta
from cosmocrat.helper_functions import deconstruct_file_path, safe_copy

def register_parser(sub_parser):
    parser_delta = sub_parser.add_parser('delta', help='Creates the delta (osm change) between two osm files')
    parser_delta.add_argument('first_input_path', action=validate_input_path)
    parser_delta.add_argument('second_input_path', action=validate_input_path)
    parser_delta.add_argument('output_path', action=validate_output_path)
    parser_delta.add_argument('-c', '--compress', action='store_true')
    parser_delta.set_defaults(func=lambda args: delta(
                                args.first_input_path,
                                args.second_input_path,
                                args.output_path,
                                args.compress))

def delta(first_input_path, second_input_path, output_path, compress):
    (_, output_name, _, _) = deconstruct_file_path(output_path)
    delta_path = create_delta(delta_path=definitions.DELTAS_PATH,
                                delta_name=output_name,
                                first_input_pbf_path=first_input_path,
                                second_input_pbf_path=second_input_path,
                                should_compress=compress)
    safe_copy(delta_path, output_path)