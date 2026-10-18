"""HTTP client for the historical OpenF1 API."""

import json
from collections.abc import Mapping, Sequence
from typing import cast
from urllib.error import HTTPError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

from f1.errors import OpenF1HTTPError, OpenF1ResponseError, OpenF1TransportError

QueryScalar = str | int | float | bool
QueryValue = QueryScalar | None | Sequence[QueryScalar]
JsonObject = dict[str, object]


class OpenF1Client:
    """Perform GET requests to OpenF1 and validate JSON record responses."""

    def __init__(
        self,
        base_url: str = "https://api.openf1.org/v1",
        timeout: float = 10.0,
    ) -> None:
        """Create a client with a validated base URL and positive timeout."""
        parsed_url = urlsplit(base_url)
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise ValueError("base_url must be an absolute HTTP or HTTPS URL")
        if parsed_url.query or parsed_url.fragment:
            raise ValueError("base_url cannot contain a query or fragment")
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")

        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    def get(
        self,
        endpoint: str,
        params: Mapping[str, QueryValue] | None = None,
    ) -> list[JsonObject]:
        """Fetch a list of JSON objects from one API endpoint."""
        if (
            not endpoint
            or endpoint.startswith("/")
            or "/" in endpoint
            or "?" in endpoint
            or "#" in endpoint
        ):
            raise ValueError("endpoint must be a single path segment")

        query = self._encode_params(params or {})
        url = f"{self._base_url}/{endpoint}"
        if query:
            url = f"{url}?{query}"
        # The base URL is HTTP(S)-only, and endpoint is restricted to one segment.
        request = Request(url, headers={"Accept": "application/json"})  # noqa: S310

        try:
            with urlopen(request, timeout=self._timeout) as response:  # noqa: S310
                payload = response.read()
        except HTTPError as error:
            raise OpenF1HTTPError(error.code, error.reason) from error
        except OSError as error:
            raise OpenF1TransportError(
                f"Could not reach OpenF1 endpoint {endpoint!r}"
            ) from error

        try:
            decoded = json.loads(payload)
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise OpenF1ResponseError(
                f"OpenF1 endpoint {endpoint!r} returned invalid JSON"
            ) from error

        if not isinstance(decoded, list) or not all(
            isinstance(record, dict) for record in decoded
        ):
            raise OpenF1ResponseError(
                f"OpenF1 endpoint {endpoint!r} must return a JSON array of objects"
            )
        return cast(list[JsonObject], decoded)

    @staticmethod
    def _encode_params(params: Mapping[str, QueryValue]) -> str:
        """Encode scalar and repeated query parameters consistently."""
        query_items: list[tuple[str, str | list[str]]] = []
        for key, value in params.items():
            if value is None:
                continue
            values = (
                value
                if isinstance(value, Sequence) and not isinstance(value, str)
                else [value]
            )
            encoded_values = [
                str(item).lower() if isinstance(item, bool) else str(item)
                for item in values
            ]
            query_items.append((key, encoded_values))
        return urlencode(query_items, doseq=True)
