# Referência da API Python

## `OpenF1Service`

Serviço de alto nível exportado por `f1`.

- `get_meetings(*, year=None, filters=None)`: consulta meetings, opcionalmente
  por temporada.
- `get_sessions(*, meeting_key=None, year=None, filters=None)`: consulta
  sessions por meeting, temporada ou ambos.
- `get_drivers(*, session_key, filters=None)`: consulta pilotos da sessão.
- `get_laps(*, session_key, filters=None)`: consulta voltas da sessão.

Os métodos retornam `list[dict[str, object]]`. `filters` aceita valores
escalares, valores repetidos e operadores de comparação no nome do parâmetro,
como documentado pela OpenF1. A repetição de um filtro já fornecido como
argumento nomeado causa `ValueError`. O argumento `session_key` é obrigatório
para consultas de pilotos e voltas.

## `OpenF1Client`

Cliente HTTP de baixo nível. Aceita `base_url` e `timeout` no construtor e
oferece `get(endpoint, params=None)`. O endpoint deve ser um segmento simples
de caminho; os parâmetros são codificados pelo cliente. É possível usar o
cliente diretamente para endpoints ainda não encapsulados no serviço, por
exemplo `get("laps", {"session_key": 9159})`.

## Lógica de voltas

`f1.laps.fastest_laps(laps, drivers)` não realiza chamadas à API. Recebe listas
de registros e retorna até cinco voltas com duração positiva, ordenadas do menor
para o maior tempo e associadas ao nome do piloto quando disponível. Cada
resultado contém `Posição`, `Piloto`, `Volta` e `Tempo (s)`.

## Exceções

- `OpenF1Error`: exceção base.
- `OpenF1TransportError`: falha de comunicação.
- `OpenF1HTTPError`: resposta HTTP malsucedida; inclui `status_code`.
- `OpenF1ResponseError`: resposta não corresponde a uma lista JSON de objetos.

Todos esses símbolos são exportados no pacote `f1`.
