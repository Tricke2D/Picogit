"""
Custom exception hierarchy for Mini Git.
"""


class MiniGitError(Exception):
    """Base exception for all Mini Git errors."""
    pass


class ObjectNotFoundError(MiniGitError):
    """Raised when an object is not found in the object store."""
    pass


class InvalidObjectTypeError(MiniGitError):
    """Raised when an object has an invalid type."""
    pass


class RepositoryNotFoundError(MiniGitError):
    """Raised when no .minigit directory is found."""
    pass