# Uso da biblioteca

## Consultar meetings

```python
from f1 import OpenF1Service

openf1 = OpenF1Service()
meetings = openf1.get_meetings(year=2023)
```

## Consultar sessions

```python
sessions = openf1.get_sessions(meeting_key=1207)
```

Também é possível filtrar por temporada:

```python
sessions = openf1.get_sessions(year=2023)
```

## Consultar pilotos

```python
drivers = openf1.get_drivers(session_key=9159)
```

Identificadores também aceitam o valor `"latest"` quando suportado pela API.
Os dados retornados são listas de dicionários; os campos disponíveis variam
conforme endpoint e sessão.

## Dashboard

Inicie a aplicação com:

```bash
poetry run streamlit run src/f1/dashboard.py
```

Selecione a temporada, o Grand Prix e a sessão para ver as cinco voltas válidas
mais rápidas, ordenadas pelo tempo, junto com o nome do piloto, o número da
volta e o tempo em segundos.

## Filtros adicionais

Use `filters` para combinar outros campos e operadores aceitos pela API:

```python
from f1 import OpenF1Client

laps = OpenF1Client().get(
    "laps",
    {"session_key": 9159, "driver_number": [4, 81], "lap_duration>=": 120},
)
```

O cliente de baixo nível demonstra o transporte genérico; endpoints fora dos
serviços principais ainda não fazem parte da interface de alto nível do MVP.

## Tratamento de erros

```python
from f1 import OpenF1Error, OpenF1Service

try:
    sessions = OpenF1Service().get_sessions(year=2023)
except OpenF1Error as error:
    print(f"Falha ao consultar a OpenF1: {error}")
```

`OpenF1HTTPError` expõe `status_code`; `OpenF1TransportError` indica uma falha
de comunicação e `OpenF1ResponseError` indica JSON ou estrutura de resposta
inválida. Em execução de produção, use `logging` em vez de `print`.
