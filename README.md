# cosmocrat-cli
A CLI tool who bundles other OSM tools functionality in one place to create simple actions.

The other OSM tools are: `osmosis`, `osmupdate` and `osmconvert`.

**Commands:**

commands have required arguments and may have optional arguments (marked with `*`), optional arguments can be specified by their flag(`-x`)

To get a short description on each command or the whole program, use the built-in help(-h) function.

- `apply` - Applies changes to a given osm file and bounds the updated result by polygon
    - input_path: path to the osm file
    - change_path: path to the osm change file
    - polygon_path: path to the poly file
    - output_path: path target to the resulting output

- `clip` - Clips an osm file by the bounds of a given polygon, the clipping is done in a OSM safe fashion meaning that all the ways and relations who are being referenced even if they are only partially inside the specified polygon or only being referenced from an entity from the inside of the polygon will be included.
    - input_path: path to the osm file
    - polygon_path: path to the poly file
    - output_path: path target to the resulting output
    - *exist_ok (-e): boolean flag, if true the result will be created only if it does not exist already in the output path. default value is false.

- `delta` - Creates the delta osm change file derieved by the changes between two osm files.
    - first_input_path: path to an osm file
    - second_input_path: path to another osm file
    - output_path: path target to the osm change file output
    - *compress (-c): boolean flag, if true the osm change result will be compressed to gzip format. default value is false.

- `drop` - Disposes of user information on the osm file. User names, user ids, changeset ids and object timestamps will be dropped from the file.
    - input_path: path to an osm file
    - *output_path (-o): path target to the dropped osm file, if output_path won't be specified the changes will occur on the input file.

- `update` - Fetches the replication files from a given source between a given time and the present. The replications will be merged into one osm change file.
    - *input_path (-i): path to an osm file, the fetch starting time will be determined according to the timestamp tag (UTC) on the file.
    input_time or timestamp must be specified.
    - *timestamp (-t): timestamp (UTC) indicating the starting time of the fetch. timestamp or input_time must be specified.
    - *source (-s): the source server replications will be fetched from. default server is the global OSM
    - *limit (-l): limit replication time units, define a list of time units the osm change output will be merged upon. default limited time units are hour and day. note that different sources can support different time units.
    - output_path: path target to the resulting osm change output
    - *output_format (-f): the format of the osm change output. choices are 'osc', 'osc.gz', 'osc.bz2'. default format is 'osc'


**Exit Codes:**

The program is invoked by command, a command can be successful or not. in any case it will exit with an exit code.
*Exit codes mapping:*

    - success: 0 - the program finished successfuly.
    - general_error: 1 - catchall for general errors.
    - osmosis_error: 100 - the program threw an exception raised by osmosis.
    - osmupdate_error: 101 - the program threw an exception raised by osmupdate.
    - osmconvert_error: 102 - the program threw an exception raised by osmconvert.
    - cannot_execute: 126 - permission problem or command is not an executable.
    - not_found: 127 - the invoked command does not exist.
    - invalid_argument: 128 - an invalid argument was given.

For additional info on given errors read the stderr output stream

**Tests:**

run tests with
```sh
python -m pytest
```

to view test coverage run
```sh
coverage run --source=. -m pytest &&
coverage report -m &&
coverage html
```
a coverage html report can be found in:
`./htmlcov/index.html`