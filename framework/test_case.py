import os
import re
import shutil

class TestCase:
    """
    The base/default implementation for a test case
    """
    def __init__(self, location) -> None:
        self.description = "" # TODO: Where should the description come from?
        self.features = [] # TODO: What features, edition of the standard, etc. does this test use?
        self.files = list(filter(
            lambda f: re.match(".*\.[fF][a-zA-Z0-9]*$", f),
            os.listdir(location))
            ) # TODO: handle C files and deal with ordering
        self.location = location
        self.other_files_on_disk = [] # TODO: What files might this test case read from?
        self.cmd_line_args = [] # TODO: Should the resulting program be executed with command line arguments?
        self.std_in_string = "" # TODO: Does the resulting program read from standard input?
        self.env_vars = {} # TODO: Do any environment variables need to be set?
        self.num_images = 1 # TODO: How many images should be launched for the program?
        self.allowed_not_to_detect = False # TODO: Is the processor allowed to not detect the error in this test case?
        self.uses_optional_feature = False # TODO: Does this case use a feature not required to be supported?
        self.uses_extension = False # TODO: Does this case use an extension to the standard?
        self.expected_outcome = None # TODO: Define outcome checkers and determine which one to use
        # The outcome checkers will likely be:
        # compile_only, failure_to_compile, compile_and_error_terminate, compile_and_terminate_normally
        # They should look at screen output (i.e. stdin + stdout), exit code,
        # other files on disc, and environment variables as appropriate

    def execute_with(self, processor, tests_path, results_path) -> None:
        result_location = self.location.replace(tests_path, results_path)
        shutil.copytree(self.location, result_location)
        outcome = processor.execute(
            self.files,
            result_location,
            self.features,
            self.other_files_on_disk,
            self.cmd_line_args,
            self.std_in_string,
            self.env_vars,
            self.num_images
            )
        # TODO: check outcome vs expected and construct some sort of result

def create_test_case(location):
    """
    This is where we figure out if we're constructing just the default behavior
    test case, or if we should pick up some special test case class.
    This should be based on whether there is a custom test case class in this
    directory, or if based on the metadata in ??? we should select
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