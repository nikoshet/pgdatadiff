"""
Usage:
  pgdatadiff --firstdb=<firstconnectionstring> --seconddb=<secondconnectionstring> [--schema=<schemaname>] [--only-data|--only-sequences] [--count-only] [--chunk-size=<size>] [--exclude-tables=<table1,table2>] [--include-tables=<table1,table2>]
  pgdatadiff --version

Options:
  -h --help          Show this screen.
  --version          Show version.
  --firstdb=postgres://postgres:password@localhost/firstdb        The connection string of the first DB
  --seconddb=postgres://postgres:password@localhost/seconddb         The connection string of the second DB
  --only-data        Only compare data, exclude sequences
  --only-sequences   Only compare seqences, exclude data
  --exclude-tables=""   Exclude tables from data comparison         Must be a comma separated string [default: ]
  --include-tables=""   Include tables in data comparison           Must be a comma separated string [default: ]
  --count-only       Do a quick test based on counts alone
  --schema=""        Compare data for specific schema
  --chunk-size=10000       The chunk size when comparing data [default: 10000]
"""

import pkg_resources
from fabulous.color import red

from pgdatadiff.pgdatadiff import DBDiff
from docopt import docopt


def main():
    arguments = docopt(
        __doc__, version=pkg_resources.require("pgdatadiff")[0].version)
    first_db_connection_string=arguments['--firstdb']
    second_db_connection_string=arguments['--seconddb']
    if not first_db_connection_string.startswith("postgres://") or \
            not second_db_connection_string.startswith("postgres://"):
        print(red("Only Postgres DBs are supported"))
        return 1

    differ = DBDiff(first_db_connection_string, second_db_connection_string,
                    schema=arguments['--schema'] or "public",
                    chunk_size=arguments['--chunk-size'],
                    count_only=arguments['--count-only'],
                    exclude_tables=arguments['--exclude-tables'],
                    include_tables=arguments['--include-tables'])

    if not arguments['--only-sequences']:
        if differ.diff_all_table_data():
            return 1
    if not arguments['--only-data']:
        if differ.diff_all_sequences():
            return 1
    return 0
