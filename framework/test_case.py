class TestCase:
    """
    The base/default implementation for a test case
    """
    def __init__(self, file, location) -> None:
        self.file = file
        self.location = location

    def execute_with(self, processor) -> None:
        processor.execute(self.file, self.location)