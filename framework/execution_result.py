"""
An object to hold the result of a processor trying to execute a test case
"""

from dataclasses import dataclass

@dataclass
class SuccessfulCompilation:
    pass

@dataclass
class CompilationFailed:
    pass

@dataclass
class ExecutionTimeout:
    pass

@dataclass
class ErrorTermination:
    return_code: int

@dataclass
class NormalTermination:
    pass

Outcome = SuccessfulCompilation | CompilationFailed | ExecutionTimeout | ErrorTermination | NormalTermination

class ExecutionResult:
    def __init__(self, outcome : Outcome, stdout : str, stderr : str) -> None:
        self.outcome = outcome
        self.stdout = stdout
        self.stderr = stderr

    def __repr__(self):
        return """
Outcome: {outcome}
stdout:
{stdout}

stderr:
{stderr}
""".format(outcome = self.outcome, stdout = self.stdout, stderr = self.stderr)