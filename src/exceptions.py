class InvalidRuleException(Exception):
    def __init__(self, message: str, line: int):
        self.message = message
        self.line = line

        super().__init__(f"Invalid rule line {line}: {message}")