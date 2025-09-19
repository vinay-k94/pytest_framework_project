class FrameworkError(Exception):
    """Base framework exception."""

class AuthError(FrameworkError):
    """Authentication/Token related errors."""

class ApiError(FrameworkError):
    """API returned unexpected response."""

class ValidationError(FrameworkError):
    """Validation failed."""
