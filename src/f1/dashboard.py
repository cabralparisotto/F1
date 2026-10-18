"""Streamlit dashboard for exploring OpenF1 data."""

from datetime import date

import streamlit as st

from f1 import OpenF1Error, OpenF1Service
from f1.clients.openf1 import JsonObject
from f1.laps import fastest_laps


def _record_key(record: JsonObject, field: str) -> int | str | None:
    """Return an API key only when its value has a supported scalar type."""
    value = record.get(field)
    if isinstance(value, str) or (
        isinstance(value, int) and not isinstance(value, bool)
    ):
        return value
    return None


def _records_with_key(records: list[JsonObject], field: str) -> list[JsonObject]:
    """Discard records that cannot be selected using the requested API key."""
    return [record for record in records if _record_key(record, field) is not None]


def _record_label(record: JsonObject, *fields: str) -> str:
    """Build a readable select-box label from available record fields."""
    values = [
        str(record[field]) for field in fields if record.get(field) not in (None, "")
    ]
    return " · ".join(values) or "Registro sem identificação"


st.set_page_config(page_title="F1 · OpenF1", page_icon="🏎️", layout="wide")
st.title("F1 · OpenF1")
st.caption("Explore meetings, sessões, voltas mais rápidas e pilotos.")

service = OpenF1Service()
year = st.selectbox(
    "Temporada",
    options=list(range(date.today().year, 2017, -1)),
)

try:
    meetings = _records_with_key(service.get_meetings(year=year), "meeting_key")
except OpenF1Error as error:
    st.error(f"Não foi possível carregar os meetings: {error}")
    st.stop()

if not meetings:
    st.info("Nenhum meeting encontrado para esta temporada.")
    st.stop()

meeting = st.selectbox(
    "Grand Prix",
    options=meetings,
    format_func=lambda record: _record_label(
        record, "meeting_name", "location", "country_name"
    ),
)
meeting_key = _record_key(meeting, "meeting_key")
if meeting_key is None:
    st.error("O meeting selecionado não contém uma chave válida.")
    st.stop()

try:
    sessions = _records_with_key(
        service.get_sessions(meeting_key=meeting_key),
        "session_key",
    )
except OpenF1Error as error:
    st.error(f"Não foi possível carregar as sessões: {error}")
    st.stop()

if not sessions:
    st.info("Nenhuma sessão encontrada para este meeting.")
    st.stop()

session = st.selectbox(
    "Sessão",
    options=sessions,
    format_func=lambda record: _record_label(
        record, "session_name", "date_start", "circuit_short_name"
    ),
)
session_key = _record_key(session, "session_key")
if session_key is None:
    st.error("A sessão selecionada não contém uma chave válida.")
    st.stop()

try:
    drivers = service.get_drivers(session_key=session_key)
except OpenF1Error as error:
    st.error(f"Não foi possível carregar os pilotos: {error}")
    st.stop()

try:
    lap_results = fastest_laps(
        service.get_laps(session_key=session_key),
        drivers,
    )
except OpenF1Error as error:
    st.error(f"Não foi possível carregar as voltas: {error}")
    st.stop()

st.subheader("5 voltas mais rápidas")
if lap_results:
    st.dataframe(lap_results, use_container_width=True, hide_index=True)
else:
    st.info("Nenhuma volta com tempo válido encontrada para esta sessão.")

st.subheader("Pilotos")
if drivers:
    st.dataframe(
        drivers,
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("Nenhum piloto encontrado para esta sessão.")
