# OpenF1 API — resumo

Este documento resume os principais recursos da API OpenF1, com foco nos endpoints e nos padrões de consulta mais úteis para explorar dados da Fórmula 1.

- **Documentação oficial:** [openf1.org/docs](https://openf1.org/docs/#api-endpoints)
- **URL base:** `https://api.openf1.org/v1`
- **Formato padrão:** JSON
- **Acesso:** dados históricos a partir de 2023 são gratuitos e não exigem autenticação. O acesso a dados em tempo real requer uma assinatura paga.

## Como fazer uma consulta

Cada recurso é acessado por uma requisição HTTP `GET`. Os parâmetros são enviados na query string:

```bash
curl "https://api.openf1.org/v1/sessions?year=2023"
```

O resultado padrão é uma lista de objetos JSON. Os campos disponíveis variam conforme o endpoint.

### Identificadores importantes

- `meeting_key`: identifica um Grande Prêmio (meeting).
- `session_key`: identifica uma sessão específica, como treino, classificação ou corrida.
- `driver_number`: número do piloto na temporada.
- `latest`: pode ser usado em `meeting_key` ou `session_key` para consultar o meeting ou a sessão mais recente/atual.

Em geral, `session_key` é o filtro mais útil para obter dados de uma sessão específica.

## Endpoints principais

| Endpoint | O que fornece |
| --- | --- |
| `/meetings` | Meetings/etapas do campeonato, com informações como local, país, circuito e temporada. |
| `/sessions` | Sessões de cada meeting, incluindo tipo da sessão e horários. |
| `/drivers` | Dados dos pilotos participantes de uma sessão, como nome, abreviação, número e equipe. |
| `/car_data` | Telemetria do carro: velocidade, acelerador, freio, marcha, RPM e estado do DRS. Amostragem aproximada de 3,7 Hz. |
| `/location` | Coordenadas e posição dos carros no circuito ao longo do tempo. |
| `/laps` | Dados de voltas, como número, duração, setores e indicadores de volta rápida ou entrada/saída dos boxes. |
| `/intervals` | Intervalo entre pilotos e diferença para o líder. Disponível somente durante corridas, com atualizações aproximadas a cada 4 segundos. |
| `/position` | Posição dos pilotos durante a sessão. |
| `/pit` | Registros de paradas nos boxes e respectivas durações. |
| `/stints` | Stints dos pilotos, incluindo composto do pneu e idade do pneu no início do stint. |
| `/weather` | Condições meteorológicas, como temperatura do ar e da pista, umidade, vento e chuva. |
| `/race_control` | Mensagens e eventos de controle de corrida, como bandeiras e incidentes reportados. |
| `/team_radio` | Trechos de comunicação de rádio entre piloto e equipe. A coleção é parcial e não representa todas as comunicações. |
| `/overtakes` | Eventos de ultrapassagem e informações sobre pilotos envolvidos e posição. |
| `/starting_grid` | Posições de largada dos pilotos. |
| `/session_result` | Resultado final da sessão, incluindo posição e situação do piloto. |
| `/championship_drivers` | Classificação do campeonato de pilotos. Recurso beta, disponível apenas para sessões de corrida. |
| `/championship_teams` | Classificação do campeonato de equipes. Recurso beta, disponível apenas para sessões de corrida. |

## Filtros

Os parâmetros de consulta filtram registros pelos atributos do endpoint. A documentação informa que é possível filtrar por qualquer atributo, exceto campos do tipo array.

Operadores numéricos e de comparação podem ser usados no nome do parâmetro, por exemplo:

```text
speed>=300
position<=3
```

Exemplo com filtros combinados:

```text
https://api.openf1.org/v1/laps?session_key=9222&driver_number=55&is_pit_out_lap=true&lap_duration%3E%3D120
```

Parâmetros repetidos também podem ser usados para consultar mais de um valor, como `driver_number=4&driver_number=81`.

### Filtros por período

Campos de data podem ser filtrados com `date_start` e `date_end`. A API aceita diversos formatos de data; ISO 8601 é uma escolha clara e não ambígua:

```text
https://api.openf1.org/v1/sessions?date_start%3E%3D2023-09-01&date_end%3C%3D2023-09-30
```

As datas e horas retornadas nos dados são, em geral, expressas em UTC e em formato ISO 8601.

## Resposta em CSV

Para receber CSV em vez de JSON, adicione `csv=true`:

```text
https://api.openf1.org/v1/sessions?year=2023&csv=true
```

Esse formato pode ser conveniente para planilhas e ferramentas de análise tabular.

## Exemplo em Python

```python
from urllib.request import urlopen
import json

url = "https://api.openf1.org/v1/sessions?year=2023"

with urlopen(url) as response:
    sessions = json.loads(response.read().decode("utf-8"))

print(sessions)
```

Para consultar a telemetria de um piloto em uma sessão, por exemplo:

```text
https://api.openf1.org/v1/car_data?session_key=9159&driver_number=55
```

## Observações

- Consulte primeiro `/meetings` e `/sessions` para localizar os identificadores antes de buscar telemetria, voltas ou posições.
- A frequência de atualização e a disponibilidade dos dados variam por endpoint e sessão.
- Os endpoints de classificação de campeonato são beta; dados de rádio são apenas uma seleção limitada.
- Verifique a documentação oficial para atributos completos, detalhes de cada campo e eventuais mudanças da API.
