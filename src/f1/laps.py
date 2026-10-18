"""Helpers for ranking OpenF1 lap records."""

from f1.clients.openf1 import JsonObject


def fastest_laps(
    laps: list[JsonObject],
    drivers: list[JsonObject],
) -> list[dict[str, object]]:
    """Return up to five valid laps ordered by duration and labeled by driver."""
    driver_names: dict[int | str, str] = {}
    for driver in drivers:
        driver_number = driver.get("driver_number")
        name = _driver_name(driver)
        if (
            isinstance(driver_number, int | str)
            and not isinstance(driver_number, bool)
            and name is not None
        ):
            driver_names[driver_number] = name

    valid_laps: list[tuple[float, JsonObject]] = []
    for lap in laps:
        duration = lap.get("lap_duration")
        if (
            isinstance(duration, int | float)
            and not isinstance(duration, bool)
            and duration > 0
        ):
            valid_laps.append((float(duration), lap))
    valid_laps.sort(key=lambda item: item[0])

    return [
        {
            "Posição": position,
            "Piloto": _lap_driver_name(driver_names, lap),
            "Volta": lap.get("lap_number", "—"),
            "Tempo (s)": f"{duration:.3f}",
        }
        for position, (duration, lap) in enumerate(valid_laps[:5], start=1)
    ]


def _lap_driver_name(driver_names: dict[int | str, str], lap: JsonObject) -> str:
    """Resolve a lap's driver number to its name, with a clear fallback."""
    driver_number = lap.get("driver_number")
    if (
        isinstance(driver_number, int | str)
        and not isinstance(driver_number, bool)
        and driver_number in driver_names
    ):
        return driver_names[driver_number]
    return _unknown_driver_name(driver_number)


def _driver_name(driver: JsonObject) -> str | None:
    """Return the best available human-readable driver name."""
    for field in ("full_name", "broadcast_name", "name_acronym"):
        name = driver.get(field)
        if isinstance(name, str) and name.strip():
            return name.strip()

    first_name = driver.get("first_name")
    last_name = driver.get("last_name")
    if isinstance(first_name, str) and isinstance(last_name, str):
        name = f"{first_name.strip()} {last_name.strip()}".strip()
        return name or None
    return None


def _unknown_driver_name(driver_number: object) -> str:
    """Label a lap clearly when its driver name is unavailable."""
    if isinstance(driver_number, int | str) and not isinstance(driver_number, bool):
        return f"Piloto #{driver_number}"
    return "Piloto desconhecido"
