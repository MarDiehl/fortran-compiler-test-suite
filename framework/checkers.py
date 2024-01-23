"""
Classes to perform checks of test case outcomes
"""

from framework.execution_result import ExecutionResult, NormalTermination
from framework.test_result import Check
import re

class NormalTerminate:
    def __init__(self, stdout : str, stderr : str, files : {str : str}):
        self.stdout = stdout
        self.stderr = stderr
        self.files = files

    def check(self, outcome : ExecutionResult):
        if isinstance(outcome.outcome, NormalTermination):
            basic_check = [Check("Successful execution", True)]
        else:
            basic_check = [Check("{outcome}, but expected normal termination".format(outcome = outcome.outcome), False)]
        return basic_check + check_screen_outputs(self.stdout, self.stderr, outcome)

class ErrorTerminate:
    def check(self, outcome : ExecutionResult):
        return [Check("tmp")]

class CompileOnly:
    def check(self, outcome : ExecutionResult):
        return [Check("tmp")]

class FailToCompile:
    def check(self, outcome : ExecutionResult):
        return [Check("tmp")]

def create_checker(expected):
    if (expected.get("compile")):
        if (expected.get("compile_only", False)):
            return CompileOnly()
        else:
            if (expected.get("normal_termination")):
                return NormalTerminate(
                    expected.get("stdout", ""),
                    expected.get("stderr", ""),
                    expected.get("output_files", {})
                )
            else:
                return ErrorTerminate()
    else:
        return FailToCompile()

def check_screen_outputs(exp_stdout, exp_stderr, outcome):
    checks = []
    if exp_stdout != "":
        if re.match(exp_stdout, outcome.stdout):
            checks.append(Check("found '{0}' in stdout".format(exp_stdout), True))
        else:
            checks.append(Check("Did not find '{0}' in stdout".format(exp_stdout), False))
    if exp_stderr != "":
        if re.match(exp_stderr, outcome.stderr):
            checks.append(Check("found '{0}' in stderr".format(exp_stderr), True))
        else:
            checks.append(Check("Did not find '{0}' in stderr".format(exp_stderr), False))
    return checks