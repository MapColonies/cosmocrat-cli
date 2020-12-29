import shutil
import cosmocrat.definitions as definitions

from cosmocrat.action_validators import validate_input_path, validate_output_path
from cosmocrat.osm_tools.osmosis import apply_changes_by_polygon
from cosmocrat.osm_tools.osmconvert import get_osm_file_timestamp, set_osm_file_timestamp

def register_parser(sub_parser):
    parser_apply = sub_parser.add_parser('apply', help='Apply changes to osm file and bound by polygon')
    parser_apply.add_argument('input_path', action=validate_input_path)
    parser_apply.add_argument('change_path', action=validate_input_path)
    parser_apply.add_argument('polygon_path', action=validate_input_path)
    parser_apply.add_argument('output_path', action=validate_output_path)
    parser_apply.set_defaults(func=lambda args: apply(
                                args.input_path,
                                args.change_path,
                                args.polygon_path,
                                args.output_path))

def apply(input_path, change_path, polygon_path, output_path):
    applied_changes_path = apply_changes_by_polygon(definitions.RESULTS_PATH,
                            input_path=input_path,
                            change_path=change_path,
                            polygon_path=polygon_path)
    changes_timestamp = get_osm_file_timestamp(change_path)
    set_osm_file_timestamp(applied_changes_path, changes_timestamp)
    shutil.copy(applied_changes_path, output_path)