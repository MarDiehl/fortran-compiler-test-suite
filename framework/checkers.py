"""
Classes to perform checks of test case outcomes
"""

from framework.execution_result import ExecutionResult, NormalTermination
from framework.test_result import Check

class NormalTerminate:
    def check(self, outcome : ExecutionResult):
        if isinstance(outcome.outcome, NormalTermination):
            return [Check("Successful execution", True)]
        else:
            return [Check("{outcome}, but expected normal termination".format(outcome = outcome.outcome), False)]

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
    # TODO: look at the configuration to determine what checker and what to look at
    return NormalTerminate()