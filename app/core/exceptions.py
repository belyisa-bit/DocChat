class DocChatException(Exception):
    """Base exception for DocChat domain errors."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class LLMProviderError(DocChatException):
    """Raised when the LLM provider fails."""

    def __init__(self, message: str):
        super().__init__(message)
