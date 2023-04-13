#!/usr/bin/env python
"""
This is the entry point for running the compiler test framework.
Usage:
    [python] run_tests.py [compiler [default-options]]
"""

import argparse

parser = argparse.ArgumentParser(
    prog="run_tests.py",
    description="Run the Fortran compiler test suite"
)
parser.add_argument('compiler', type=str, nargs=1)
parser.add_argument('default-options', type=str, nargs=1)

print("hello")