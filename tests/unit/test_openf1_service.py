"""Unit tests for OpenF1 query services."""

from collections.abc import Callable
from unittest.mock import Mock

import pytest

from f1.clients.openf1 import OpenF1Client
from f1.services.openf1 import OpenF1Service


def test_get_meetings_passes_season_and_filters() -> None:
    """Pass meeting filters to the API client."""
    client = Mock(spec=OpenF1Client)
    client.get.return_value = [{"year": 2023}]
    service = OpenF1Service(client)

    result = service.get_meetings(year=2023, filters={"country_name": "Italy"})

    assert result == [{"year": 2023}]
    client.get.assert_called_once_with(
        "meetings",
        {"year": 2023, "country_name": "Italy"},
    )


def test_get_sessions_passes_meeting_and_year() -> None:
    """Pass meeting and season identifiers to the API client."""
    client = Mock(spec=OpenF1Client)
    service = OpenF1Service(client)

    service.get_sessions(meeting_key=1207, year=2023)

    client.get.assert_called_once_with(
        "sessions",
        {"meeting_key": 1207, "year": 2023},
    )


def test_get_drivers_requires_session_key() -> None:
    """Query driver metadata by session key."""
    client = Mock(spec=OpenF1Client)
    service = OpenF1Service(client)

    service.get_drivers(session_key="latest")

    client.get.assert_called_once_with("drivers", {"session_key": "latest"})


def test_get_laps_passes_session_key() -> None:
    """Query lap records for the selected session."""
    client = Mock(spec=OpenF1Client)
    service = OpenF1Service(client)

    service.get_laps(session_key=9159)

    client.get.assert_called_once_with("laps", {"session_key": 9159})


@pytest.mark.parametrize(
    ("query", "params"),
    [
        (
            lambda service: service.get_meetings(
                year=2023,
                filters={"year": 2024},
            ),
            "year",
        ),
        (
            lambda service: service.get_sessions(
                meeting_key=1207,
                filters={"meeting_key": 1300},
            ),
            "meeting_key",
        ),
        (
            lambda service: service.get_drivers(
                session_key=9159,
                filters={"session_key": 9158},
            ),
            "session_key",
        ),
        (
            lambda service: service.get_laps(
                session_key=9159,
                filters={"session_key": 9158},
            ),
            "session_key",
        ),
    ],
)
def test_service_rejects_duplicate_filters(
    query: Callable[[OpenF1Service], object],
    params: str,
) -> None:
    """Reject duplicate reserved filter names rather than silently overriding."""
    service = OpenF1Service(Mock(spec=OpenF1Client))

    with pytest.raises(ValueError, match=params):
        query(service)
