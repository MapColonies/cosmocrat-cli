import shutil

from cosmocrat.action_validators import validate_input_path
from cosmocrat.osm_tools.osmconvert import drop_author

def register_parser(sub_parser):
    parser_drop = sub_parser.add_parser('drop', help='Drops user information from the OSM file')
    parser_drop.add_argument('input_path', action=validate_input_path)
    parser_drop.set_defaults(func=lambda args: drop(args.input_path))

def drop(input_path):
    drop_author(input_path)