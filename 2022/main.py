#!/usr/bin/env python3

import tools.aoc
import argparse
import importlib
import os

YEAR = 2022
TIMEIT_NUMBER = 50

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("-d", "--day", help="specify day to process; leave empty for ALL days", type=int)
argument_parser.add_argument("-p", "--part", help="run only part x", choices=[1, 2], type=int)
argument_parser.add_argument("--timeit", help="measure execution time", action="store_true", default=False)
argument_parser.add_argument(
    "--timeit-number",
    help="build average time over this many executions",
    type=int,
    default=TIMEIT_NUMBER
)
argument_parser.add_argument("-v", "--verbose", help="show test case outputs", action="store_true", default=False)
flags = argument_parser.parse_args()

import_day = ""
if flags.day:
    import_day = "%02d" % flags.day

imported = []
for _, _, files in os.walk(tools.aoc.BASE_PATH):
    for f in files:
        if f.startswith('day' + import_day) and f.endswith('.py'):
            lib_name = f[:-3]
            globals()[lib_name] = importlib.import_module(lib_name)
            imported.append(lib_name)

    break

for lib in sorted(imported):
    day = int(lib[-2:])
    day_class = getattr(globals()[lib], "Day")(YEAR, day)
    day_class.run(flags.part if flags.part else 3, flags.verbose, flags.timeit, flags.timeit_number)
