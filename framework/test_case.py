import os
import re

class TestCase:
    """
    The base/default implementation for a test case
    """
    def __init__(self, files, location) -> None:
        self.files = files
        self.location = location

    def execute_with(self, processor) -> None:
        processor.execute(self.files, self.location)

def create_test_case(location):
    """
    This is where we should figure out if we're constructing just the default behavior
    test case, or if we should pick up some special test case class.
    This should be based on whether there is a custom test case class in this
    directory, or if based on the metadata in the source code we should select
    one of our specialized test cases.
    """
    files = os.listdir(location)
    fortran_files = list(filter(lambda f: re.match(".*\.[fF][a-zA-Z0-9]*$", f), files))
    return TestCase(fortran_files, location)