import os
import tempfile

from enum import Enum
from MapColoniesJSONLogger.logger import generate_logger

app_name = 'cosmocrat-cli'

OSMOSIS_PATH='/usr/bin/osmosis'
OSMUPDATE_PATH='/usr/bin/osmupdate'
OSMCONVERT_PATH='/usr/bin/osmconvert'

Time_Unit = Enum('Time_Unit', 'minute hour day week')
Subprocess_Tool = Enum('Subprocess_Tool', 'osmosis osmupdate osmconvert')

TEMP_PATH = tempfile.gettempdir()
TEMP_APP_PATH = os.path.join(TEMP_PATH, app_name)
DATA_PATH = os.path.join(TEMP_APP_PATH, 'data')
OSMCHANGES_PATH = os.path.join(DATA_PATH, 'osm-changes')
RESULTS_PATH = os.path.join(DATA_PATH, 'results')
DELTAS_PATH = os.path.join(DATA_PATH, 'deltas')
POLYGONS_PATH = os.path.join(DATA_PATH, 'polygons')
OSMUPDATE_CACHE_PATH = os.path.join(DATA_PATH, 'osmupdate_temp', 'temp')

TIME_UNITS_IN_USE = ['hour', 'day']
REPLICATION_SERVER_BASE_URL='https://planet.openstreetmap.org/replication'
TIMESTAMP_REGEX = r'\b[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}\:[0-9]{2}\:[0-9]{2}Z\b'
FORMATS_MAP = {
    'OSM_PBF': 'osm.pbf',
    'OSM': 'osm',
    'OSC': 'osc',
    'OSC_GZ': 'osc.gz',
    'OSC_BZ2': 'osc.bz2',
    'POLY': 'poly'
}
COMPRESSION_METHOD_MAP = {
    'osc': 'none',
    'gz': 'gzip',
    'osc.gz': 'gzip',
    'bz2': 'bzip2',
    'osc.bz2': 'bzip2'
}
EXIT_CODES = {
    'success': 0,
    'general_error': 1,
    'osmosis_error': 100,
    'osmupdate_error': 101,
    'osmconvert_error': 102,
    'cannot_execute': 126,
    'not_found': 127,
    'invalid_argument': 128
}

log_file_extention = '.log'
base_log_path = os.path.join('/var', 'log', app_name)
service_logs_path = os.path.join(base_log_path, app_name + log_file_extention)
os.makedirs(base_log_path, exist_ok=True)
log = generate_logger(app_name, log_level='INFO', handlers=[{'type': 'rotating_file', 'path': service_logs_path},{ 'type': 'stream', 'output': 'stderr' }])