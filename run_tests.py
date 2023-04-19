#!/usr/bin/env python
"""
This is the entry point for running the compiler test framework.
Usage:
    [python] run_tests.py [compiler [default-options]]
"""

import argparse
import os
import re
import shutil
from framework.processor import Processor
from framework.test_case import create_test_case, RESULTS_PATH, TESTS_PATH

parser = argparse.ArgumentParser(
    prog="run_tests.py",
    description="Run the Fortran compiler test suite"
)
parser.add_argument('compiler', nargs='?', default="gfortran")
parser.add_argument('default_options', nargs='*')
args = parser.parse_args()

processor = Processor(args.compiler, args.default_options)
if (os.path.exists(RESULTS_PATH)): shutil.rmtree(RESULTS_PATH)
os.mkdir(RESULTS_PATH)

for root, dirs, files in os.walk(TESTS_PATH):
    if any([re.match(".*\.[fF][a-zA-Z0-9]*$", f) for f in files]): # Are any files Fortran?
        test_case = create_test_case(root)
        test_case.execute_with(processor)
        # TODO: capture the results and figure out how to organize, display and/or save them