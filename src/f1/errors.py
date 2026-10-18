"""Exceptions raised by the F1 package."""


class OpenF1Error(Exception):
    """Base exception for errors communicating with OpenF1."""


class OpenF1TransportError(OpenF1Error):
    """Raised when a request cannot reach the OpenF1 API."""


class OpenF1HTTPError(OpenF1Error):
    """Raised when the OpenF1 API returns an unsuccessful HTTP status."""

    def __init__(self, status_code: int, reason: str) -> None:
        """Store the status code and a concise HTTP reason."""
        self.status_code = status_code
        super().__init__(f"OpenF1 returned HTTP {status_code}: {reason}")


class OpenF1ResponseError(OpenF1Error):
    """Raised when an API response is not valid JSON records."""
