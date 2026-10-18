"""Convenience operations for the initial OpenF1 data scope."""

from collections.abc import Mapping

from f1.clients.openf1 import JsonObject, OpenF1Client, QueryValue


class OpenF1Service:
    """Expose meeting, session, driver, and lap queries using an OpenF1 client."""

    def __init__(self, client: OpenF1Client | None = None) -> None:
        """Use the supplied client or construct a default OpenF1 client."""
        self._client = client if client is not None else OpenF1Client()

    def get_meetings(
        self,
        *,
        year: int | None = None,
        filters: Mapping[str, QueryValue] | None = None,
    ) -> list[JsonObject]:
        """Return meetings, optionally filtered by season and other fields."""
        params = self._merge_filters({"year": year}, filters)
        return self._client.get("meetings", params)

    def get_sessions(
        self,
        *,
        meeting_key: int | str | None = None,
        year: int | None = None,
        filters: Mapping[str, QueryValue] | None = None,
    ) -> list[JsonObject]:
        """Return sessions, optionally filtered by meeting or season."""
        params = self._merge_filters(
            {"meeting_key": meeting_key, "year": year},
            filters,
        )
        return self._client.get("sessions", params)

    def get_drivers(
        self,
        *,
        session_key: int | str,
        filters: Mapping[str, QueryValue] | None = None,
    ) -> list[JsonObject]:
        """Return drivers participating in the selected session."""
        params = self._merge_filters({"session_key": session_key}, filters)
        return self._client.get("drivers", params)

    def get_laps(
        self,
        *,
        session_key: int | str,
        filters: Mapping[str, QueryValue] | None = None,
    ) -> list[JsonObject]:
        """Return lap records for the selected session."""
        params = self._merge_filters({"session_key": session_key}, filters)
        return self._client.get("laps", params)

    @staticmethod
    def _merge_filters(
        required_filters: Mapping[str, QueryValue],
        filters: Mapping[str, QueryValue] | None,
    ) -> dict[str, QueryValue]:
        """Merge explicit query fields and reject ambiguous duplicate keys."""
        merged = dict(filters or {})
        for key, value in required_filters.items():
            if value is None:
                continue
            if key in merged:
                raise ValueError(f"filter {key!r} was provided more than once")
            merged[key] = value
        return merged
