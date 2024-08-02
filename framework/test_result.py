"""
Classes to hold and format the results of a test case
"""

class Check:
    def __init__(self, description: str, passed: bool):
        self.description = description
        self.passed = passed

    def __repr__(self):
        return "\"{d}: {p}\"".format(d = self.description, p = "passed" if self.passed else "failed")

class TestResult:
    def __init__(self, title : str, features : [str], checks : [Check], commands : [str], stdout : str, stderr : str, allowed_failure : bool):
        self.title = title
        self.features = features
        self.checks = checks
        self.commands = commands
        self.stdout = stdout
        self.stderr = stderr
        self.allowed_failure = allowed_failure

    def failed(self):
        return not all([c.passed for c in self.checks])

    def failing_checks(self):
        return filter(lambda c: not c.passed, self.checks)

    def __repr__(self):
        return """
Case: {title}
Features: {features}
Passed: {passed}
Failure Acceptable? {accept}
Checks: {checks}
commands:
{commands}

stdout:
{stdout}

stderr:
{stderr}
""".format(
            title = self.title,
            features = self.features,
            passed = not self.failed(),
            accept = "yes" if self.allowed_failure else "no",
            checks = self.checks,
            commands = "\n".join(self.commands),
            stdout = self.stdout,
            stderr = self.stderr
)