import shutil
import cosmocrat.definitions as definitions

from cosmocrat.action_validators import validate_input_path, validate_output_path
from cosmocrat.osm_tools.osmosis import clip_polygon
from cosmocrat.osm_tools.osmconvert import get_osm_file_timestamp, set_osm_file_timestamp

def register_parser(sub_parser):
    parser_clip = sub_parser.add_parser('clip', help='Clips a polygon out of osm file')
    parser_clip.add_argument('input_path', action=validate_input_path)
    parser_clip.add_argument('polygon_path', action=validate_input_path)
    parser_clip.add_argument('output_path', action=validate_output_path)
    parser_clip.add_argument('-e', '--exist_ok', action='store_true')
    parser_clip.set_defaults(func=lambda args: clip(
                                args.input_path,
                                args.polygon_path,
                                args.output_path,
                                args.exist_ok))

def clip(input_path, polygon_path, output_path, exist_ok):
    timestamp = get_osm_file_timestamp(input_path)
    clipped_path = clip_polygon(input_path=input_path,
                                polygon_path=polygon_path,
                                input_timestamp=timestamp,
                                base_output_path=definitions.RESULTS_PATH,
                                exist_ok=exist_ok)
    set_osm_file_timestamp(clipped_path, timestamp)
    shutil.copy(clipped_path, output_path)