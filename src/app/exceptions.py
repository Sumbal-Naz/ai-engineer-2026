class InvalidProjectIDError(Exception):
    """Raised when an invalid project ID is provided."""
    pass


class ModelNotFoundError(Exception):
    """Raised when an AI model does not exist."""
    pass


class DuplicateModelError(Exception):
    """Raised when an AI model already exists."""
    pass
