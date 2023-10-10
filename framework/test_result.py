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
    def __init__(self, title, features, checks, stdout, stderr, allowed_failure):
        self.title = title
        self.features = features
        self.checks = checks
        self.stdout = stdout
        self.stderr = stderr
        self.allowed_failure = allowed_failure

    def __repr__(self):
        return """
Case: {title}
Features: {features}
Passed: {passed}
Failure Acceptable? {accept}
Checks: {checks}
stdout:
{stdout}

stderr:
{stderr}
""".format(
            title = self.title,
            features = self.features,
            passed = all([c.passed for c in self.checks]),
            accept = "yes" if self.allowed_failure else "no",
            checks = self.checks,
            stdout = self.stdout,
            stderr = self.stderr
)