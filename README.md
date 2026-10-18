# F1

Biblioteca Python para consultar dados históricos da [OpenF1](https://openf1.org/).
O MVP oferece consultas a meetings, sessions e pilotos, sem autenticação ou
dependências HTTP de produção.

## Requisitos

- Python 3.12 ou superior
- Poetry 2.x

## Instalação

```bash
poetry install
```

## Exemplo

```python
from f1.services.openf1 import OpenF1Service

openf1 = OpenF1Service()
meetings = openf1.get_meetings(year=2023)
sessions = openf1.get_sessions(meeting_key=1207)
drivers = openf1.get_drivers(session_key=9158)
```

Os métodos retornam listas de dicionários decodificados do JSON da API. Falhas de
rede, respostas HTTP de erro e respostas inválidas são reportadas como exceções
`OpenF1Error`; elas não são convertidas silenciosamente em listas vazias.

## Desenvolvimento

```bash
poetry run task test
poetry run task lint
poetry run task format
poetry run task docs
poetry run task docs-build
poetry run task dashboard
```

`format` aplica o Ruff Formatter nos arquivos Python; para apenas verificar o
formato sem modificá-los, use `poetry run task format-check`.
`dashboard` inicia a aplicação Streamlit em `src/f1/dashboard.py`.
`docs` inicia o servidor local do MkDocs, abre a documentação no navegador e
atualiza as páginas durante a edição. Para apenas validar/gerar o site sem
iniciar o servidor, use `poetry run task docs-build`.

Consulte a [documentação](docs/index.md) para instalação, arquitetura, camadas
do dashboard F1, uso, desenvolvimento, próximos passos e referência da API.
