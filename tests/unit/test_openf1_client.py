"""Unit tests for the OpenF1 HTTP client."""

from io import BytesIO
from unittest.mock import patch
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlsplit

import pytest

from f1.clients.openf1 import OpenF1Client
from f1.errors import OpenF1HTTPError, OpenF1ResponseError, OpenF1TransportError


def test_get_encodes_filters_and_repeated_values() -> None:
    """Encode query filters and return decoded records."""
    payload = BytesIO(b'[{"driver_number": 55}]')

    with patch("f1.clients.openf1.urlopen", return_value=payload) as open_url:
        records = OpenF1Client().get(
            "laps",
            {
                "session_key": 9159,
                "driver_number": [4, 81],
                "is_pit_out_lap": True,
                "lap_duration>=": 120,
                "unused": None,
            },
        )

    request = open_url.call_args.args[0]
    assert records == [{"driver_number": 55}]
    assert open_url.call_args.kwargs == {"timeout": 10.0}
    assert parse_qs(urlsplit(request.full_url).query) == {
        "session_key": ["9159"],
        "driver_number": ["4", "81"],
        "is_pit_out_lap": ["true"],
        "lap_duration>=": ["120"],
    }


@pytest.mark.parametrize(
    ("base_url", "timeout"),
    [
        ("relative/path", 10.0),
        ("https://api.openf1.org/v1?format=json", 10.0),
        ("https://api.openf1.org/v1#fragment", 10.0),
        ("https://api.openf1.org/v1", 0.0),
    ],
)
def test_client_rejects_invalid_configuration(base_url: str, timeout: float) -> None:
    """Reject invalid base URLs and non-positive timeouts."""
    with pytest.raises(ValueError, match=r"base_url|timeout"):
        OpenF1Client(base_url=base_url, timeout=timeout)


@pytest.mark.parametrize("endpoint", ["", "/sessions", "sessions/drivers", "laps?x=1"])
def test_get_rejects_non_endpoint_path(endpoint: str) -> None:
    """Prevent callers from injecting path, query, or fragment components."""
    with pytest.raises(ValueError, match="single path segment"):
        OpenF1Client().get(endpoint)


@pytest.mark.parametrize(
    "payload",
    [
        b"not-json",
        b'{"session_key": 1}',
        b"[1, 2]",
    ],
)
def test_get_rejects_invalid_json_shapes(payload: bytes) -> None:
    """Require valid JSON arrays containing only objects."""
    with (
        patch("f1.clients.openf1.urlopen", return_value=BytesIO(payload)),
        pytest.raises(OpenF1ResponseError),
    ):
        OpenF1Client().get("sessions")


def test_get_translates_http_error() -> None:
    """Expose unsuccessful HTTP status codes as package errors."""
    http_error = HTTPError(
        "https://api.openf1.org/v1/sessions",
        429,
        "Too Many Requests",
        None,
        None,
    )
    with (
        patch("f1.clients.openf1.urlopen", side_effect=http_error),
        pytest.raises(OpenF1HTTPError, match="429") as error,
    ):
        OpenF1Client().get("sessions")

    assert error.value.status_code == 429


def test_get_translates_transport_error() -> None:
    """Expose transport failures without pretending the request succeeded."""
    with (
        patch(
            "f1.clients.openf1.urlopen",
            side_effect=URLError("connection refused"),
        ),
        pytest.raises(OpenF1TransportError, match="Could not reach OpenF1"),
    ):
        OpenF1Client().get("sessions")
