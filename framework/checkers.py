"""
Classes to perform checks of test case outcomes
"""

from framework.execution_result import (
    ExecutionResult,
    ErrorTermination,
    SuccessfulCompilation,
    NormalTermination
)
from framework.test_result import Check
import re
import os

class NormalTerminate:
    def __init__(self, stdout : [str], stderr : [str], either : [str], files : {str : [str]}):
        self.stdout = stdout
        self.stderr = stderr
        self.either = either
        self.files = files

    def check(self, outcome : ExecutionResult, location : str):
        if isinstance(outcome.outcome, NormalTermination):
            basic_check = [Check("Successful execution", True)]
        else:
            basic_check = [Check("{outcome}, but expected normal termination".format(outcome = outcome.outcome), False)]
        return (
            basic_check 
            + check_screen_outputs(self.stdout, self.stderr, outcome)
            + check_either_outputs(self.either, outcome)
            + check_additional_files(self.files, location)
        )

class ErrorTerminate:
    def __init__(self, stdout : [str], stderr : [str], either : [str], exit_code : int):
        self.stdout = stdout
        self.stderr = stderr
        self.either = either
        self.exit_code = exit_code

    def check(self, outcome : ExecutionResult, location : str):
        if isinstance(outcome.outcome, ErrorTermination):
            if (self.exit_code == 0):
                basic_check = [Check("Error terminated as expected", True)]
            else:
                if (self.exit_code == outcome.outcome.return_code):
                    basic_check = [Check("Expected and received exit code {0}".format(self.exit_code), True)]
                else:
                    basic_check = [Check("Expected exit code {0}, but was {1}".format(self.exit_code, outcome.outcome.return_code), False)]
        else:
            basic_check = [Check("{outcome}, but expected error termination".format(outcome = outcome.outcome), False)]
        return (
            basic_check
            + check_screen_outputs(self.stdout, self.stderr, outcome)
            + check_either_outputs(self.either, outcome)
        )

class CompileOnly:
    def __init__(self, stdout : [str], stderr : [str], either : [str]):
        self.stdout = stdout
        self.stderr = stderr
        self.either = either

    def check(self, outcome : ExecutionResult, location : str):
        if isinstance(outcome.outcome, SuccessfulCompilation):
            basic_check = [Check("Successfully Compiled", True)]
        else:
            basic_check = [Check("{outcome}, but expected successful compilation".format(outcome = outcome.outcome), False)]
        return (
            basic_check 
            + check_screen_outputs(self.stdout, self.stderr, outcome)
            + check_either_outputs(self.either, outcome)
        )

class FailToCompile:
    def check(self, outcome : ExecutionResult, location : str):
        return [Check("tmp")]

def create_checker(expected):
    if (expected.get("compile")):
        if (expected.get("compile_only", False)):
            return CompileOnly(expected.get("stdout", []), expected.get("stderr", []), expected.get("either_output", []))
        else:
            if (expected.get("normal_termination")):
                return NormalTerminate(
                    expected.get("stdout", []),
                    expected.get("stderr", []),
                    expected.get("either_output", []),
                    expected.get("output_files", {})
                )
            else:
                return ErrorTerminate(
                    expected.get("stdout", []), 
                    expected.get("stderr", []), 
                    expected.get("either_output", []), 
                    expected.get("exit_code", 0))
    else:
        return FailToCompile()

def check_screen_outputs(exp_stdout : [str], exp_stderr : [str], outcome : ExecutionResult):
    checks = []
    for expr in exp_stdout:
        if re.match(expr, outcome.stdout):
            checks.append(Check("Found '{0}' in stdout".format(expr), True))
        else:
            checks.append(Check("Did not find '{0}' in stdout".format(expr), False))
    for expr in exp_stderr:
        if re.match(expr, outcome.stderr):
            checks.append(Check("Found '{0}' in stderr".format(expr), True))
        else:
            checks.append(Check("Did not find '{0}' in stderr".format(expr), False))
    return checks

def check_either_outputs(expected : [str], outcome : ExecutionResult):
    checks = []
    for expr in expected:
        if re.match(expr, outcome.stdout):
            checks.append(Check("Found '{0}' in stdout".format(expr), True))
        elif re.match(expr, outcome.stderr):
            checks.append(Check("Found '{0}' in stderr".format(expr), True))
        else:
            checks.append(Check("Did not find '{0}' in either stdout or stderr".format(expr), False))
    return checks

def check_additional_files(file_checks : {str : [str]}, location : str):
    checks = []
    for file, exprs in file_checks.items():
        file_path = os.path.join(location, file)
        if os.path.isfile(file_path):
            with open(os.path.join(location, file), 'r') as f:
                contents = f.read()
                for expr in exprs:
                    if (re.match(expr, contents)):
                        checks.append(Check("Found '{0}' in '{1}'".format(expr, file), True))
                    else:
                        checks.append(Check("Did not find '{0}' in '{1}'".format(expr, file), False))
        else:
            checks.append(Check("Expected file '{0}' did not exist".format(file)), False)
    return checks
