class InvalidProjectIDError(Exception):
    """Raised when an invalid project ID is provided."""


class ModelNotFoundError(Exception):
    """Raised when an AI model does not exist."""


class DuplicateModelError(Exception):
    """Raised when an AI model already exists."""
