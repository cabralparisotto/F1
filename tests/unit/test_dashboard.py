"""Tests for the Streamlit OpenF1 dashboard."""

from pathlib import Path

from streamlit.testing.v1 import AppTest

from f1.clients.openf1 import JsonObject
from f1.laps import fastest_laps
from f1.services.openf1 import OpenF1Service


def test_fastest_laps_sorts_valid_times_and_returns_at_most_five() -> None:
    """Ignore invalid lap times and select the five shortest valid durations."""
    laps: list[JsonObject] = [
        {"driver_number": 7, "lap_number": 1, "lap_duration": 92.0},
        {"driver_number": 4, "lap_number": 2, "lap_duration": 88.125},
        {"driver_number": 8, "lap_number": 3, "lap_duration": None},
        {"driver_number": 1, "lap_number": 4, "lap_duration": 90},
        {"driver_number": 5, "lap_number": 5, "lap_duration": 91.5},
        {"driver_number": 3, "lap_number": 6, "lap_duration": 89.75},
        {"driver_number": 2, "lap_number": 7, "lap_duration": 90.5},
        {"driver_number": 9, "lap_number": 8, "lap_duration": 0},
    ]

    drivers: list[JsonObject] = [
        {"driver_number": 4, "full_name": "Charles Leclerc"},
        {"driver_number": 3, "full_name": "Daniel Ricciardo"},
        {"driver_number": 1, "full_name": "Max Verstappen"},
        {"driver_number": 2, "full_name": "Logan Sargeant"},
        {"driver_number": 5, "full_name": "Sebastian Vettel"},
    ]

    fastest = fastest_laps(laps, drivers)

    assert len(fastest) == 5
    assert [lap["Tempo (s)"] for lap in fastest] == [
        "88.125",
        "89.750",
        "90.000",
        "90.500",
        "91.500",
    ]
    assert [lap["Piloto"] for lap in fastest] == [
        "Charles Leclerc",
        "Daniel Ricciardo",
        "Max Verstappen",
        "Logan Sargeant",
        "Sebastian Vettel",
    ]


def test_fastest_laps_uses_driver_identifier_when_name_is_unavailable() -> None:
    """Keep a useful driver label when the OpenF1 driver name is missing."""
    laps: list[JsonObject] = [
        {"driver_number": 44, "lap_number": 1, "lap_duration": 90.0}
    ]

    assert fastest_laps(laps, []) == [
        {
            "Posição": 1,
            "Piloto": "Piloto #44",
            "Volta": 1,
            "Tempo (s)": "90.000",
        }
    ]


def test_dashboard_displays_openf1_records(monkeypatch) -> None:
    """Render meeting, session, lap, and driver data without network access."""
    monkeypatch.setattr(
        OpenF1Service,
        "get_meetings",
        lambda self, *, year=None, filters=None: [
            {
                "meeting_key": 1,
                "meeting_name": "Grand Prix",
                "location": "Monza",
                "country_name": "Italy",
            }
        ],
    )
    monkeypatch.setattr(
        OpenF1Service,
        "get_sessions",
        lambda self, *, meeting_key=None, year=None, filters=None: [
            {
                "session_key": 10,
                "session_name": "Race",
                "date_start": "2023-09-03",
                "circuit_short_name": "Monza",
            }
        ],
    )
    monkeypatch.setattr(
        OpenF1Service,
        "get_laps",
        lambda self, *, session_key, filters=None: [
            {"driver_number": 1, "lap_number": 4, "lap_duration": 91.234}
        ],
    )
    monkeypatch.setattr(
        OpenF1Service,
        "get_drivers",
        lambda self, *, session_key, filters=None: [
            {"driver_number": 1, "full_name": "Max Verstappen"}
        ],
    )

    dashboard_path = Path(__file__).resolve().parents[2] / "src/f1/dashboard.py"
    app = AppTest.from_file(str(dashboard_path)).run(timeout=10)

    assert not app.exception
    assert len(app.selectbox) == 3
    assert len(app.dataframe) == 2
