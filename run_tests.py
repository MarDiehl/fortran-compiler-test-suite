#!/usr/bin/env python
"""
This is the entry point for running the compiler test framework.
Usage:
    [python] run_tests.py [compiler [default-options]]
"""

import os
import re
import shutil
import sys
from framework.processor import Processor
from framework.test_case import create_test_case, RESULTS_PATH, TESTS_PATH

if (any(opt == '-h' or opt == '--help' for opt in sys.argv)):
    print("Usage: [python] run_tests.py [-h] [compiler [default_options ...]]")
else:
    if (len(sys.argv) > 1):
        compiler = sys.argv[1]
        if (len(sys.argv) > 2):
            default_opts = sys.argv[2:]
        else:
            default_opts = []
    else:
        compiler = "gfortran"

    processor = Processor(compiler, default_opts)
    if (os.path.exists(RESULTS_PATH)): shutil.rmtree(RESULTS_PATH)
    os.mkdir(RESULTS_PATH)

    for root, dirs, files in os.walk(TESTS_PATH):
        if any([re.match(".*\.[fF][a-zA-Z0-9]*$", f) for f in files]): # Are any files Fortran?
            test_case = create_test_case(root)
            test_case.execute_with(processor)
            # TODO: capture the results and figure out how to organize, display and/or save them