# Desenvolvimento

## Ambiente e dependências

Use a versão de Python compatível com `requires-python` e gerencie o ambiente e
as dependências exclusivamente com Poetry:

```bash
poetry install
poetry env info
```

Não instale dependências do projeto com `pip` nem globalmente. Ao alterar
dependências, atualize `pyproject.toml` com Poetry e versione `poetry.lock`.
Para ativar os hooks de pre-commit no clone local, execute uma vez:

```bash
poetry install
poetry run pre-commit install
```

O pre-commit fornece feedback rápido localmente e não substitui o GitHub
Actions. O hook `ruff-check` corrige lint e imports automaticamente (`--fix`),
e `ruff-format` também pode modificar arquivos. Se algum hook fizer alterações,
revise-as e adicione os arquivos novamente com `git add` antes de commitar.
Os hooks de Pytest são manuais para manter o fluxo normal de commit rápido; o CI
continua executando os testes unitários e a cobertura mínima de 50%.

Para executar os hooks em todos os arquivos:

```bash
poetry run pre-commit run --all-files
```

Para executar validações específicas ou os testes sob demanda:

```bash
poetry run pre-commit run ruff-check --all-files
poetry run pre-commit run ruff-format --all-files
poetry run pre-commit run --hook-stage manual pytest --all-files
```

Para atualizar as versões fixadas dos hooks, remover o hook deste clone ou
limpar os ambientes em cache do pre-commit:

```bash
poetry run pre-commit autoupdate
poetry run pre-commit uninstall
poetry run pre-commit clean
```

## Iniciar a documentação

Na raiz do repositório, execute:

```bash
poetry run task docs
```

Esse comando compila a documentação em modo estrito, inicia o servidor de
desenvolvimento do MkDocs e abre o site no navegador em `http://127.0.0.1:8000/`.
O servidor observa os arquivos em `docs/` e atualiza o site quando eles mudam.
Encerre-o com `Ctrl+C`.

Para validar o build sem iniciar o servidor ou abrir o navegador:

```bash
poetry run task docs-build
```

## Qualidade e testes

```bash
poetry run task test
poetry run task lint
poetry run task format
poetry run task docs
poetry run task docs-build
poetry run task dashboard
```

As tarefas são definidas em `[tool.taskipy.tasks]` no `pyproject.toml`. `test`
executa pytest com cobertura mínima de 50%; `lint` executa Ruff; `format` aplica
o formatter; `docs` serve a documentação e `docs-build` gera o site em modo
estrito. Para validar a formatação sem alterar arquivos, use a tarefa
`format-check`, como faz o CI.

As regras de lint, formatação, pytest e cobertura ficam centralizadas em
`pyproject.toml`. Mantenha código de produção em `src/f1/` e testes em `tests/`.
Testes unitários devem isolar as chamadas externas e usar respostas sintéticas.
`task dashboard` é um atalho para iniciar a interface Streamlit; a dashboard
permite consultar meetings, sessões, pilotos e voltas da OpenF1 por temporada.

O GitHub Actions executa lint, verificação de formatação, testes com cobertura e
build estrito da documentação em cada push e pull request. Também é possível
iniciar a pipeline manualmente pela aba Actions do GitHub.

## Convenções

- Use type hints e docstrings no padrão Google para APIs públicas.
- Mantenha interface, integração HTTP e regras de domínio em responsabilidades
  distintas. Veja [arquitetura e camadas](architecture.md).
- Faça erros de transporte e resposta aparecerem explicitamente; não esconda
  falhas nem retorne sucesso fictício.
- Atualize esta documentação quando a instalação, arquitetura ou operação mudar.
