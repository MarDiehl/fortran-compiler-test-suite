Community-Driven Fortran Compiler Test Suite
============================================

This repository contains a framework and suite of cases for testing a Fortran compiler with the primary goals of

1. Making it easy for the Fortran community to add tests and
2. Making it easy to use the framework with a broad range of compilers.

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

# Contributing a Test

At an appropriate location with the `tests` directory

* create a folder with an appropriate name with contents
* a `config.yml` file with contents as outlined below
* the appropriate source file(s)

## Contents of a `config.yml` file

The `config.yml` file contains YAML formatted data defining the attributes of the test case.
YAML is a fairly well standardized format, which you can find a good description of [here](https://yaml.org/spec/1.2.2/).
Briefly, it is a file that contains a list of key-value pairs, where the values may be arrays of values, or themselves lists of key-value pairs.
This framework expects to find the following keys.

* `description`, required - A string that describes the features of the test case
* `features`, optional - An array of strings identifying various features of the language being tested
* `source_files`, required - An array of strings identifying the source files, in the order in which they are to be compiled
* `other_files`, optional - An array of strings identifying any additional files needed by the test case
* `command_line_arguments`, optional - An array of strings which should be passed as command line arguments when running the resulting executable
* `standard_input`, optional - A string which should be provided as standard input when running the resulting executable
* `environment_variables`, optional - A set of key-value pairs, where the key is the name of the environment variable, and the value is what it's value should be when running the resulting executable
* `num_images`, optional - The number of images that the resulting executable should be launched with
* `allowed_not_to_detect`, optional, default=`false` - `true` or `false` defining whether a processor is allowed to not detect a violation of the standard
* `uses_optional_feature`, optional, default=`false` - `true` or `false` defining whether the test case uses a feature of the language not required to be supported
* `uses_extension`, optional, default=`false` - `true` or `false` defining whether the test case uses a feature not defined by the standard
* `expected`, required - A set of key-value pairs describing the expected behavior of the test case
  * `compile`, required - `true` or `false`, the code should successfully compile
  * `compiler_error`, optional - If `compile` is `false`, an array of regular expressions that the output should match
  * `compile_only`, optional, default=`false` - If `true`, do not attempt to run the resulting executable
  * `normal_termination`, required iff `compile` is `true` and `compile_only` is `false` - `true` if the resulting executable should terminate with an exit code of 0 when run
  * `exit_code`, optional, default=0 - an integer specifying the expected exit code if `normal_termination` is false
  * `stdout`, optional - an array of regular expressions that should match the output produced to standard output by running the resulting executable
  * `stderr`, optional - an array of regular expressions that should match the output produced to standard error by running the resulting executable
  * `output_files`, optional - A set of key-value pairs where the key is the name of a file expected to be output, and the value is an array of regular expressions expected to match the contents of that file.

<!--
TODO: Should there be a way for a test case to specify that it needs particular compiler
      flags for a given compiler?
-->

# Anatomy of a Good Test Case

A test case should be small and focused.
It should include a small subset of the features of the language,
ideally focused on testing a single feature, constraint, or syntax element.
To the extent possible, let the framework check the outputs as this should provide maximum feedback to users of the test suite.
Minimize the size of the config file, i.e. only specify what is required and relevant.
