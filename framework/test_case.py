import os
import re
import shutil

RESULTS_PATH = "results"
TESTS_PATH = "tests"

class TestCase:
    """
    The base/default implementation for a test case
    """
    def __init__(self, location) -> None:
        self.files = list(filter(
            lambda f: re.match(".*\.[fF][a-zA-Z0-9]*$", f),
            os.listdir(location))
            )
        self.location = location

    def execute_with(self, processor) -> None:
        result_location = self.location.replace(TESTS_PATH, RESULTS_PATH)
        shutil.copytree(self.location, result_location)
        processor.execute(self.files, result_location)

def create_test_case(location):
    """
    This is where we should figure out if we're constructing just the default behavior
    test case, or if we should pick up some special test case class.
    This should be based on whether there is a custom test case class in this
    directory, or if based on the metadata in the source code we should select
    one of our specialized test cases.
    """
    case = make_case_specific_class(location)
    if not case is None: return case
    case = make_special_class(location)
    if not case is None: return case
    return TestCase(location)

def make_case_specific_class(location):
    """
    See if there is a python file (name?) that we should import and instantiate
    a TestCase from it
    """
    return None

def make_special_class(location):
    """
    Look at the "features" of the test case and see if there is some aspect
    of it that falls into a "special" case that we have a different implementation for.
    """
    return None