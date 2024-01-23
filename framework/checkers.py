"""
Classes to perform checks of test case outcomes
"""

from framework.execution_result import ExecutionResult, NormalTermination
from framework.test_result import Check

class JustNormalTermination:
    def check(self, outcome : ExecutionResult):
        if isinstance(outcome.outcome, NormalTermination):
            return [Check("Successful execution", True)]
        else:
            return [Check("{outcome}, but expected normal termination".format(outcome = outcome.outcome), False)]

def create_checker(expected):
    # TODO: look at the configuration to determine what checker and what to look at
    return JustNormalTermination()