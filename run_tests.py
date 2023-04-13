#!/usr/bin/env python
"""
This is the entry point for running the compiler test framework.
Usage:
    [python] run_tests.py [compiler [default-options]]
"""

import argparse
import os
import re
from framework.test_case import TestCase

parser = argparse.ArgumentParser(
    prog="run_tests.py",
    description="Run the Fortran compiler test suite"
)
parser.add_argument('compiler', type=str, nargs=1)
parser.add_argument('default-options', type=str, nargs=1)

for root, dirs, files in os.walk("tests"):
    fortran_files = list(filter(lambda f: re.match(".*\.[fF][a-zA-Z0-9]*$", f), files))
    if any(fortran_files): # Are any files Fortran?
        print("Found fortran in: ", root, " they are: ", fortran_files)
        for file in fortran_files:
            test_case = TestCase(file, root)
            test_case.execute()
