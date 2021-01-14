import os

EMPTY_STRING=''
FILE_PATH='/tmp/cosmocrat-cli/data'
FILE_NAME='output'
FILE_FORMAT='osm.pbf'
FAKE_MULTI_PURPOSE='xyz'
FULL_FILE_PATH=os.path.join(FILE_PATH, f'{FILE_NAME}.{FILE_FORMAT}')