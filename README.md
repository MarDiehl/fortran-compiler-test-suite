Community-Driven Fortran Compiler Test Suite
============================================

This repository contains a framework and suite of cases for testing a Fortran compiler with primary goals of

1. Making it easy for the Fortran community to add tests and
2. Making it easy to use the framework with a broad  range of compilers.

# Usage

```text
usage: run_tests.py [-h] [-i INPUT] [-o OUTPUT] [-c COMPILER] [-f FLAGS [FLAGS ...]]

Run the Fortran compiler test suite

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Directory to search for the tests (default: tests)
  -o OUTPUT, --output OUTPUT
                        Where to put the test results (default: results)
  -c COMPILER, --compiler COMPILER
                        The compiler to test (default: gfortran)
  -f FLAGS [FLAGS ...], --flags FLAGS [FLAGS ...]
                        The default flags to use for compilation (default: None)
```