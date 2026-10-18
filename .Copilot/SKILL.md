---
name: python-data-engineering-development
description: "Guia oficial para desenvolver, testar, empacotar e documentar projetos Python de Engenharia de Dados usando Poetry, Ruff, pytest, cobertura e MkDocs Material."
---

# Desenvolvimento Python para Engenharia de Dados

## Nome da skill

**Python Data Engineering Development** — padrão oficial para desenvolvimento, manutenção e entrega de projetos Python da equipe de Engenharia de Dados.

## Objetivo

Estabelecer regras reproduzíveis para arquitetura, dependências, qualidade, testes, cobertura, documentação e integração contínua. O guia define comandos executáveis e critérios de aceite para que alterações sejam consistentes, seguras, testáveis e fáceis de operar.

## Escopo

Aplica-se ao código de produção, testes, pipelines, documentação e automações deste projeto. O código Python de produção fica em `src/projeto/`; ajuste o nome `projeto` nos exemplos ao nome de importação configurado no `pyproject.toml`. Neste checkout, o pacote existente é `f1` em `src/f1/`; enquanto esse nome for mantido, use `f1` nos argumentos `--cov` e nas configurações que identificam o pacote.

## Princípios obrigatórios

- O Poetry é a ferramenta oficial para dependências, ambiente virtual, execução de comandos, empacotamento e manutenção do lockfile.
- Dependências do projeto são declaradas no `pyproject.toml`; `poetry.lock` é versionado junto com as alterações correspondentes.
- Não utilizar `pip install`, não instalar dependências do projeto globalmente e não usar `pip` para instalar ferramentas de desenvolvimento.
- Executar ferramentas do projeto preferencialmente com `poetry run`.
- Código de produção reside em `src/`; testes ficam separados em `tests/`.
- Alterações de comportamento incluem testes relevantes e, quando necessário, atualização da documentação.
- Ruff, pytest com cobertura mínima de 50% e build estrito do MkDocs devem passar localmente e no CI/CD.
- Segredos, credenciais, dados pessoais e arquivos locais sensíveis nunca devem ser versionados.

## Estrutura do projeto

Use uma estrutura `src/` para separar o pacote instalável dos arquivos de suporte:

```text
projeto/
├── pyproject.toml
├── poetry.lock
├── README.md
├── .gitignore
├── .env.example
├── mkdocs.yml
├── src/
│   └── projeto/
│       ├── __init__.py
│       ├── config/
│       ├── domain/
│       ├── models/
│       ├── pipelines/
│       ├── ingestion/
│       ├── transformation/
│       ├── validation/
│       ├── storage/
│       ├── clients/
│       ├── repositories/
│       ├── services/
│       ├── utils/
│       └── cli.py
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── fixtures/
│   └── conftest.py
├── docs/
│   ├── index.md
│   ├── installation.md
│   ├── architecture.md
│   ├── development.md
│   ├── pipelines.md
│   ├── testing.md
│   ├── contributing.md
│   └── api/
└── scripts/
```

Regras da estrutura:

- Todo código de produção pertence a `src/projeto/`; não misture testes, notebooks exploratórios ou scripts operacionais dentro do pacote sem justificativa.
- Testes não devem ficar misturados ao código de produção. Mantenha testes unitários e de integração em diretórios distintos.
- Cada módulo deve ter responsabilidade única e granularidade compatível com o domínio; evite módulos monolíticos e a fragmentação sem propósito.
- Mantenha alto acoplamento conceitual dentro de um módulo (alta coesão) e baixo acoplamento entre módulos.
- Evite dependências circulares. Dependências devem apontar para abstrações estáveis, não para camadas de nível superior.
- Regras de negócio não devem depender diretamente de serviços, bancos, formatos de arquivos ou detalhes de infraestrutura.
- Integrações externas devem ser isoladas atrás de interfaces, clientes, adaptadores ou repositórios.
- Pipelines devem combinar componentes pequenos, independentes e testáveis; separe orquestração da lógica de negócio.
- Configurações, credenciais e parâmetros de execução não devem ser codificados diretamente no código.
- Favoreça transformações determinísticas, reprocessamento seguro, idempotência, observabilidade e rastreabilidade.

## Arquitetura modular para Engenharia de Dados

Organize o fluxo de dados em etapas explícitas, com contratos definidos entre elas:

1. **Ingestão:** obtenha dados por meio de clientes/adaptadores, registrando origem, horário, parâmetros e identificadores de execução.
2. **Validação:** valide schema, tipos, campos obrigatórios, chaves, domínios, nulidade, unicidade e regras de qualidade pertinentes antes de avançar.
3. **Transformação:** implemente regras de domínio em funções/componentes pequenos, com entradas e saídas explícitas e resultados determinísticos sempre que possível.
4. **Persistência:** isole escrita e leitura em interfaces de armazenamento; defina atomicidade, particionamento, estratégia de atualização e tratamento de falhas.
5. **Orquestração:** coordene etapas, dependências, parâmetros e retentativas sem concentrar as regras de negócio no orquestrador.

Boas práticas de desenho:

- Represente dados e contratos com tipos, dataclasses, modelos validados ou estruturas equivalentes adequadas ao domínio.
- Versione schemas e contratos de dados quando consumidores dependem deles; documente mudanças incompatíveis e migrações.
- Torne as operações idempotentes quando reexecutar uma partição, arquivo ou janela não puder duplicar ou corromper resultados.
- Prefira processamento incremental quando reduzir custo e latência sem comprometer correção; documente checkpoints, watermark e política de backfill.
- Faça o tratamento de erros explícito: diferencie falha transitória, dado inválido, configuração ausente e violação de contrato. Registre contexto suficiente para diagnóstico sem expor segredos ou conteúdo sensível.
- Use logs estruturados com identificador de execução, pipeline, etapa, fonte/destino, partição e métricas relevantes. Use `logging`, não `print`.
- Configure comportamento por ambiente e injete parâmetros em tempo de execução; não dependa de configurações ocultas ou estado global mutável.
- Considere volume, cardinalidade, custo de I/O, paralelismo e uso de memória. Evite carregar conjuntos inteiros em memória quando processamento em lotes ou streaming for apropriado.
- Garanta que o mesmo input e a mesma configuração produzam resultado equivalente, salvo quando a fonte ou a regra de negócio justificar explicitamente variação.
- Meça e registre contagens de entrada/saída, descartes, rejeições e duração, respeitando privacidade e segurança.

## Uso obrigatório do Poetry

Poetry é a única interface autorizada para gerenciar dependências do projeto, criar e gerenciar seu ambiente virtual, executar ferramentas, empacotar e manter o arquivo de lock. Não instale dependências do projeto globalmente.

### Instalação e configuração

Instale o Poetry por um método oficial compatível com o sistema operacional (instalador oficial ou gerenciador de ferramentas aprovado pela equipe), sem usar `pip` para instalar pacotes do projeto. Consulte a documentação oficial do Poetry para obter o instalador atualizado. Depois, confirme a instalação:

```bash
poetry --version
```

O projeto requer uma versão de Python compatível com `requires-python` em `pyproject.toml` (neste checkout, `>=3.12`). Instale/sele a versão adequada com o gerenciador de Python aprovado pela equipe. Se `pyenv` estiver adotado:

```bash
pyenv install --list
pyenv install 3.12.10
pyenv local 3.12.10
python --version
```

`3.12.10` é um exemplo; use uma versão suportada e compatível com `pyproject.toml`. Para iniciar um projeto vazio ou adicionar configuração a um repositório:

```bash
poetry new --src projeto
```

Ou, na raiz de um projeto existente sem `pyproject.toml`:

```bash
poetry init
```

Não execute `poetry new` sobre um projeto já inicializado. Confirme que o Poetry está selecionando o interpretador esperado:

```bash
poetry env use "$(pyenv which python)"
poetry run python --version
```

Se `pyenv` não for utilizado, passe ao `poetry env use` o caminho do interpretador aprovado para o projeto.

### Instalação de dependências e comandos

Configure o ambiente virtual dentro do projeto antes de criá-lo:

```bash
poetry config virtualenvs.in-project true --local
poetry install
```

Para instalar apenas as dependências de produção:

```bash
poetry install --only main
```

Para incluir o grupo de desenvolvimento:

```bash
poetry install --with dev
```

Execute ferramentas sempre que possível pelo ambiente do projeto:

```bash
poetry run ruff check .
poetry run pytest
poetry run mkdocs serve
```

### Regras sobre o uso de pip

- **Nunca utilizar `pip install`**, inclusive para instalar ferramentas de lint, testes, documentação ou qualquer outro pacote usado pelo projeto.
- **Nunca instalar dependências do projeto globalmente** nem depender de uma instalação global para que os comandos funcionem.
- Toda dependência usada pelo projeto deve ser declarada no `pyproject.toml`, no grupo correto, e resolvida pelo Poetry.
- Instalação, remoção, atualização e sincronização de dependências do projeto são feitas pelos comandos `poetry add`, `poetry remove`, `poetry update` e `poetry install`.
- `poetry.lock` deve ser versionado. Não edite o lockfile manualmente; mantenha-o sincronizado pelo Poetry e revise-o junto com `pyproject.toml`.
- Ferramentas são executadas preferencialmente por `poetry run`; não use executáveis globais como substitutos do ambiente do projeto.

### Gerenciamento do ambiente virtual

```bash
# Ativar/configurar o interpretador do ambiente
poetry env use "$(pyenv which python)"

# Consultar o diretório do ambiente
poetry env info --path

# Consultar detalhes do ambiente e a versão do Python
poetry env info
poetry run python --version

# Executar um shell dentro do ambiente
poetry run bash
```

Para ativação interativa em Bash, o Poetry também pode imprimir o comando de ativação:

```bash
poetry env activate
```

Execute no shell atual o comando apresentado. Em Bash/Linux, com o ambiente virtual dentro do projeto:

```bash
source "$(poetry env info --path)/bin/activate"
deactivate
```

Prefira `poetry run` em scripts, CI e instruções documentadas para manter a execução explícita e reproduzível.

### Gerenciamento de dependências

Dependências necessárias em produção pertencem ao grupo principal. Ruff, pytest, pytest-cov e MkDocs pertencem ao grupo `dev`:

```bash
# Adicionar dependência de produção
poetry add nome-do-pacote

# Adicionar ferramenta de desenvolvimento
poetry add --group dev nome-da-ferramenta

# Exemplos de ferramentas
poetry add --group dev ruff
poetry add --group dev pytest pytest-cov
poetry add --group dev mkdocs mkdocs-material

# Remover dependência de produção ou de desenvolvimento
poetry remove nome-do-pacote
poetry remove --group dev nome-da-ferramenta

# Atualizar todas as dependências ou uma dependência específica
poetry update
poetry update nome-do-pacote

# Regenerar/sincronizar o lockfile após mudanças no pyproject.toml
poetry lock
poetry install

# Ver dependências instaladas e suas relações
poetry show
poetry show --tree
```

Faça commit de `pyproject.toml` e `poetry.lock` juntos quando as dependências mudarem. Antes de aprovar a atualização, valide instalação, testes e ferramentas de qualidade.

## Configuração centralizada no pyproject.toml

Use o arquivo `pyproject.toml` como fonte central das dependências, empacotamento e configurações de qualidade. O exemplo abaixo supõe pacote `projeto` em `src/projeto/` e Python 3.12 ou superior; alinhe o requisito e o alvo Ruff à versão oficial realmente suportada pelo repositório.

```toml
[project]
name = "projeto"
version = "0.1.0"
description = "Pipelines e componentes de Engenharia de Dados"
readme = "README.md"
requires-python = ">=3.12"
dependencies = []

[tool.poetry]
packages = [{ include = "projeto", from = "src" }]

[tool.poetry.group.dev.dependencies]
ruff = ">=0.11,<1.0"
pytest = ">=8.0,<9.0"
pytest-cov = ">=6.0,<7.0"
mkdocs = ">=1.6,<2.0"
mkdocs-material = ">=9.5,<10.0"

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.ruff]
line-length = 88
target-version = "py312"
src = ["src", "tests"]
extend-exclude = [
    ".git",
    ".venv",
    "build",
    "dist",
    "htmlcov",
    "site",
]

[tool.ruff.lint]
select = [
    "E",       # estilo pycodestyle
    "W",       # avisos pycodestyle
    "F",       # erros Pyflakes
    "I",       # organização de imports
    "B",       # bugs comuns (flake8-bugbear)
    "UP",      # modernização compatível com a versão alvo
    "SIM",     # simplificações seguras
    "N",       # convenções de nomenclatura
    "ASYNC",   # boas práticas assíncronas
    "S",       # práticas de segurança, avaliadas no contexto
    "PT",      # boas práticas de pytest
    "D",       # docstrings
    "RUF",     # regras específicas do Ruff
]
fixable = ["ALL"]
unfixable = []

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["S101"]

[tool.ruff.lint.isort]
known-first-party = ["projeto"]
combine-as-imports = true

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "lf"
docstring-code-format = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-ra"

[tool.coverage.run]
source = ["projeto"]
branch = true
relative_files = true
omit = [
    "*/__pycache__/*",
    "*/generated/*",
]

[tool.coverage.report]
fail_under = 50
show_missing = true
skip_covered = true
precision = 1
```

Notas de configuração:

- `packages = [{ include = "projeto", from = "src" }]` informa ao Poetry qual pacote empacotar. `source = ["projeto"]` e `--cov=projeto` identificam o módulo importável para a cobertura; `--cov=src/projeto` pode identificar o caminho físico.
- O nome de distribuição (`project.name`), o nome importável do pacote e o argumento de cobertura podem diferir. O nome importável normalmente corresponde ao diretório dentro de `src/`, não necessariamente ao nome da distribuição. Use o pacote real deste repositório, atualmente `f1`, em `packages`, `known-first-party`, `source` e `--cov` enquanto esse for o nome configurado.
- `branch = true` mede também os caminhos condicionais; por isso, o percentual pode ser menor que uma medição apenas de linhas.
- Não exclua código para atingir a meta. Exclua código gerado ou genuinamente não testável somente com justificativa explícita, configuração estreita e revisão no Pull Request.
- `--fix` aplica correções seguras, mas não deve ocultar mudanças comportamentais. Revise sempre o diff gerado.

## Configuração e uso do Ruff

Ruff é a ferramenta oficial para linting, formatação e organização/correção de imports. Mantenha sua configuração no `pyproject.toml`; não crie configurações concorrentes em arquivos paralelos sem decisão técnica registrada.

Significado dos conjuntos selecionados:

- `E`, `W`: estilo e avisos compatíveis com pycodestyle.
- `F`: erros detectados pelo Pyflakes.
- `I`: organização e ordenação de imports.
- `B`: padrões associados a bugs comuns.
- `UP`: modernização da sintaxe respeitando a versão alvo do Python.
- `SIM`: simplificações de código.
- `N`: convenções de nomes.
- `ASYNC`: boas práticas de programação assíncrona.
- `S`: práticas de segurança. Avalie alertas segundo o contexto e não os ignore sem justificativa.
- `PT`: boas práticas para testes pytest.
- `D`: convenções de docstrings definidas como Google.
- `RUF`: regras específicas do Ruff.

`line-length = 88` define a largura adotada. `target-version` deve coincidir com o menor Python suportado, e `extend-exclude` evita verificar saídas geradas. O formatter usa aspas duplas, indentação por espaços e finais de linha Unix; alterações de estilo devem ser aplicadas pelo Ruff, não por formatadores concorrentes.

Comandos oficiais:

```bash
# Verificar lint em todo o repositório
poetry run ruff check .

# Corrigir automaticamente o que for seguro, incluindo imports
poetry run ruff check . --fix

# Formatar o código
poetry run ruff format .

# Validar a formatação sem modificar arquivos
poetry run ruff format --check .

# Verificar explicitamente produção e testes
poetry run ruff check src tests
poetry run ruff check src tests --fix
```

Execute o Ruff durante o fluxo local, antes de abrir um Pull Request e no CI/CD. Verifique código de produção e testes, incluindo ordenação de imports. O CI deve validar formatação sem aplicar mudanças.

## Padrões de lint, formatação e imports

- Mantenha uma importação por grupo: biblioteca padrão, dependências externas e módulos locais; deixe Ruff/isort ordenar os grupos.
- Evite imports curingas e imports locais redundantes. Use imports absolutos do pacote para tornar dependências entre módulos claras.
- Não suprima regras com `noqa` sem necessidade comprovada. Quando inevitável, use a regra específica e explique o motivo.
- Configure exceções por arquivo ou diretório com escopo mínimo; não desative uma regra globalmente apenas para liberar uma ocorrência.
- Formate `src/`, `tests/` e demais arquivos Python mantidos pelo time de acordo com a configuração central.
- Resolva alertas de segurança avaliando entradas, segredos, subprocessos, serialização e caminhos de arquivo; uma supressão não substitui análise.

## Testes unitários com Pytest

Instale pytest e pytest-cov como dependências de desenvolvimento:

```bash
poetry add --group dev pytest
poetry add --group dev pytest-cov
```

Organize testes em `tests/unit/` e `tests/integration/`. Use `tests/conftest.py` para fixtures compartilhadas e `tests/fixtures/` para arquivos de dados pequenos, controlados e não sensíveis. Nomeie arquivos `test_<modulo>.py` e funções `test_<comportamento>`.

Critérios de qualidade:

- Teste comportamento observável e contratos públicos, não detalhes internos que podem mudar sem alterar o comportamento.
- Cubra casos de sucesso, erros esperados, limites, dados ausentes, entradas inválidas e regras de domínio relevantes.
- Teste isoladamente transformações, validações e regras de negócio; testes unitários não devem depender de rede, banco, serviço externo ou credencial real.
- Use fixtures para setup e teardown, com escopo mínimo e sem estado compartilhado mutável inesperado.
- Use `pytest.mark.parametrize` para conjuntos de casos que verificam a mesma regra com entradas distintas.
- Use mocks apenas nas fronteiras externas ou quando uma dependência real for inadequada; não simule em excesso a própria lógica sob teste.
- Mantenha testes determinísticos, independentes da ordem, de horário, aleatoriedade e estado externo. Fixe relógio/semente ou injete dependências quando necessário.
- Reserve testes de integração para validar a interação de componentes, com serviços e dados de teste controlados.

Exemplos de execução:

```bash
poetry run pytest
poetry run pytest tests/unit
poetry run pytest tests/unit/test_modulo.py
poetry run pytest -k nome_do_teste
poetry run pytest -v
poetry run pytest --maxfail=1
```

## Meta de cobertura mínima de 50%

A cobertura mínima obrigatória é **50% para o código de `src/projeto/`**. Valide o resultado localmente e no CI/CD:

```bash
# Cobertura apontando para o caminho de origem
poetry run pytest --cov=src/projeto --cov-report=term-missing

# Cobertura apontando para o módulo importável
poetry run pytest --cov=projeto --cov-report=term-missing

# Relatório HTML em htmlcov/
poetry run pytest --cov=projeto --cov-report=html

# Falhar se a cobertura total ficar abaixo de 50%
poetry run pytest --cov=projeto --cov-fail-under=50
```

Substitua `projeto` pelo pacote real. As opções podem ser combinadas:

```bash
poetry run pytest --cov=projeto --cov-report=term-missing --cov-report=html --cov-fail-under=50
```

Interpretação dos relatórios:

- **Cobertura de linhas:** proporção de linhas executáveis que foram executadas pelos testes.
- **Cobertura de branches:** proporção de caminhos de decisão (por exemplo, ramos de `if`) percorridos. Ative com `branch = true`.
- **Cobertura geral:** percentual agregado sobre o escopo informado em `source` ou `--cov`; é esse percentual total que deve atingir pelo menos 50%.
- **Cobertura de módulos específicos:** mostra a execução por arquivo/módulo e ajuda a localizar áreas descobertas; não substitui a meta agregada do pacote.

Cobertura não deve ser obtida com testes artificiais, assertions triviais ou exclusões indevidas. Todo módulo ou funcionalidade nova deve vir acompanhado de testes de comportamento. A meta é elevar progressivamente cobertura e qualidade. Código gerado e trechos justificadamente não testáveis só podem ser excluídos com justificativa e configuração explícita, estreita e revisada.

## Documentação com MkDocs Material

Adicione as ferramentas ao grupo de desenvolvimento:

```bash
poetry add --group dev mkdocs
poetry add --group dev mkdocs-material
```

Mantenha páginas em `docs/` e navegação/configuração na raiz, em `mkdocs.yml`. Configuração inicial recomendada:

```yaml
site_name: Projeto de Engenharia de Dados
site_url: https://exemplo.invalid/documentacao/
docs_dir: docs
site_dir: site
strict: true

theme:
  name: material
  language: pt
  features:
    - navigation.sections
    - navigation.top
    - content.code.copy

nav:
  - Visão geral: index.md
  - Instalação: installation.md
  - Arquitetura: architecture.md
  - Desenvolvimento: development.md
  - Pipelines: pipelines.md
  - Testes: testing.md
  - Contribuição: contributing.md
  - Referência técnica: api/index.md

plugins:
  - search

markdown_extensions:
  - admonition
  - attr_list
  - md_in_html
  - toc:
      permalink: true
  - pymdownx.details
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format

validation:
  links:
    absolute_links: warn
    anchors: warn
    unrecognized_links: warn
```

Substitua a URL de exemplo pela URL real quando existir. Para aplicar `nav`, crie as páginas correspondentes; remova entradas que não se aplicam ou adicione arquivos de referência técnica/API conforme o projeto evoluir. MkDocs Material oferece suporte a código e a diagramas Mermaid por meio das extensões configuradas. Corrija avisos de links; com `strict: true`, avisos no build devem ser tratados como falhas.

O conjunto mínimo de documentação deve cobrir:

- visão geral, objetivos, limites e componentes do projeto;
- instalação, versão do Python, ambiente e dependências;
- configuração por ambiente e uso seguro de variáveis de ambiente;
- arquitetura, contratos, schemas e decisões técnicas relevantes;
- desenvolvimento local, qualidade, lint e convenções;
- execução, parâmetros, reprocessamento e operação dos pipelines;
- testes unitários, integração e cobertura;
- contribuição, revisão, versionamento e Pull Requests;
- troubleshooting com sintomas, diagnóstico e solução;
- referência técnica/API quando aplicável.

Comandos:

```bash
# Servidor local com recarga automática
poetry run mkdocs serve

# Gerar o site estático em site/
poetry run mkdocs build

# Validar links e avisos; falhar quando houver avisos
poetry run mkdocs build --strict
```

No CI/CD, publique o diretório gerado `site/` somente após o build estrito passar e de acordo com o processo aprovado para o ambiente de destino. Nunca inclua credenciais, dados reais sensíveis ou arquivos `.env` no site.

## Boas práticas de Python

- **Type hints:** anote parâmetros, retornos e estruturas públicas; use tipos específicos, `Protocol` ou tipos de domínio em vez de tipos vagos quando isso melhorar o contrato.
- **Compatibilidade:** implemente somente recursos compatíveis com a versão mínima oficial do Python definida em `requires-python` e em `target-version`.
- **Docstrings:** documente propósito, parâmetros, retorno, exceções relevantes e efeitos colaterais de APIs públicas e componentes não óbvios. Siga a convenção Google configurada no Ruff.
- **Nomenclatura:** use nomes explícitos; `snake_case` para funções/variáveis, `PascalCase` para classes e `UPPER_SNAKE_CASE` para constantes.
- **Funções e classes:** mantenha escopo e responsabilidade pequenos; extraia unidades quando melhorarem compreensão, reuso ou testabilidade, não apenas para reduzir linhas.
- **Exceções:** capture tipos específicos e trate falhas na camada que consegue tomar uma ação. Não utilize `except Exception` sem justificativa documentada e necessidade concreta; não oculte erros nem retorne sucesso fictício.
- **Valores e estado:** substitua valores mágicos por constantes nomeadas ou configuração validada. Evite estado global mutável e efeitos colaterais implícitos.
- **Modelagem:** use `dataclasses`, `Enum` e `Protocol` quando expressarem dados, estados ou contratos de forma simples e útil; não introduza abstrações sem necessidade.
- **Logs:** use `logging` com nível adequado e contexto estruturado; não use `print` em código de produção.
- **Segredos e configuração:** injete configuração por variáveis de ambiente ou mecanismo seguro da plataforma; forneça apenas placeholders em `.env.example`; nunca registre ou versione segredos.
- **Validação:** valide entradas nas fronteiras do sistema e converta-as para tipos/representações internos explícitos.
- **Ferramentas estáticas:** mantenha código compatível com Ruff e com as verificações estáticas adotadas pelo projeto; não suprima alertas sem justificativa.
- **Arquivos e recursos:** use `pathlib.Path` para caminhos e context managers (`with`) para arquivos, conexões e recursos que precisam de encerramento.
- **APIs internas:** preserve contratos estáveis ou documente migrações quando uma mudança incompatível for inevitável.
- **Revisão:** revise clareza, segurança, impacto operacional, testes, documentação e diff antes de solicitar aprovação.
- **Versionamento:** use versionamento semântico quando o projeto publica versões de pacote/API. Faça commits pequenos e objetivos, com mensagens claras.
- **Pull Requests:** mantenha escopo focado, descreva contexto, solução, validações e riscos; divida mudanças grandes em partes revisáveis.
- **Decisões técnicas:** registre decisões duradouras e trade-offs em documentação apropriada (por exemplo, ADR), não apenas em mensagens de chat.

## Boas práticas específicas de Engenharia de Dados

- Mantenha ingestão, validação, transformação e persistência como responsabilidades distintas e observáveis.
- Defina contratos de entrada e saída: schema, tipos, unidade, timezone, semântica de nulos, chaves e regras de qualidade.
- Valide schema e qualidade antes de gravar dados finais; reporte rejeições com causa e métricas, sem descartar falhas silenciosamente.
- Use modelos/tipos para representar registros e fronteiras, e schemas versionados para contratos compartilhados.
- Isole conectores, clientes e armazenamento; injete-os na lógica para permitir testes sem serviços externos.
- Projete pipelines para reprocessamento e idempotência; especifique comportamento para duplicatas, retentativas e execuções parciais.
- Separe código de orquestração de regras de domínio e de transformação.
- Adote processamento incremental, particionamento e checkpoints quando aplicáveis; documente como executar backfill com segurança.
- Controle memória e performance com lotes/streaming apropriados ao volume; meça antes de otimizar e evite cópias desnecessárias de grandes estruturas.
- Torne parâmetros de execução explícitos, validados e rastreáveis; identifique cada execução e registre suas métricas.
- Trate explicitamente erros de origem, schema, transformação e destino. Diferencie erros recuperáveis de falhas que exigem interrupção.
- Nunca inclua dados de produção em fixtures versionadas. Use dados sintéticos ou anonimizados e mínimos.
- Preserve privacidade: minimize dados pessoais em logs e relatórios; aplique retenção e acesso conforme as políticas do projeto.

## Fluxo local de desenvolvimento

1. Clone o repositório e entre na raiz.
2. Instale/selecione a versão de Python declarada pelo projeto.
3. Confirme que Poetry usa essa mesma versão e configure o ambiente virtual do projeto.
4. Instale dependências com Poetry.
5. Crie ou atualize uma branch de trabalho focada.
6. Implemente a funcionalidade modularmente, respeitando contratos e fronteiras.
7. Execute Ruff para lint, imports e formatação; revise as correções automáticas.
8. Crie ou atualize testes unitários e, se necessário, testes de integração.
9. Execute os testes e investigue falhas sem enfraquecer as assertions.
10. Valide cobertura total mínima de 50%.
11. Atualize documentação MkDocs para mudanças de instalação, operação, arquitetura ou API.
12. Construa a documentação em modo estrito.
13. Revise o diff, os arquivos de dependência/lock e a ausência de segredos/dados sensíveis.
14. Abra o Pull Request somente depois de todas as validações passarem.

Exemplo de sequência executável; substitua os placeholders do repositório:

```bash
git clone <url-do-repositorio>
cd <nome-do-projeto>

poetry config virtualenvs.in-project true --local
poetry env use "$(pyenv which python)"
poetry install

git switch -c feat/descricao-curta

poetry run ruff check .
poetry run ruff format --check .
poetry run pytest --cov=projeto --cov-report=term-missing --cov-fail-under=50
poetry run mkdocs build --strict

git status --short
git diff --check
git diff
```

Se não usar `pyenv`, substitua o caminho do interpretador na configuração do ambiente pelo caminho aprovado. Se a formatação ou `ruff check --fix` alterar arquivos, revise o diff e repita as validações. Faça commit do lockfile se dependências forem modificadas.

## Integração contínua

O CI/CD deve usar uma versão de Python compatível com o projeto, instalar Poetry por um método oficial e reproduzir o ambiente a partir dos arquivos versionados. No mínimo, execute:

```bash
poetry install
poetry run ruff check .
poetry run ruff format --check .
poetry run pytest --cov=projeto --cov-report=term-missing --cov-fail-under=50
poetry run mkdocs build --strict
```

O pipeline deve falhar quando houver erro de lint, código fora do formato, falha de teste, cobertura total inferior a 50%, dependências inconsistentes ou documentação que não possa ser construída em modo estrito. Não aplique formatação automaticamente no CI: valide e solicite que a alteração seja corrigida no branch. Use cache de dependências somente sem comprometer a reprodutibilidade e nunca exponha segredos nos logs.

## Comandos rápidos

```bash
# Ambiente e dependências
poetry install
poetry install --only main
poetry env info --path
poetry show --tree

# Qualidade e imports
poetry run ruff check .
poetry run ruff check . --fix
poetry run ruff format .
poetry run ruff format --check .

# Testes e cobertura obrigatória
poetry run pytest
poetry run pytest tests/unit
poetry run pytest --cov=projeto --cov-report=term-missing --cov-fail-under=50
poetry run pytest --cov=projeto --cov-report=html

# Documentação
poetry run mkdocs serve
poetry run mkdocs build
poetry run mkdocs build --strict
```

## Checklist de Pull Request

- [ ] Mudança tem escopo claro, descrição e impacto operacional documentados.
- [ ] Código de produção permanece em `src/projeto/` e segue responsabilidades modulares.
- [ ] Configuração, credenciais e parâmetros não foram codificados no código.
- [ ] Dependências foram adicionadas/removidas com Poetry e declaradas em `pyproject.toml`.
- [ ] `poetry.lock` foi atualizado e versionado quando necessário.
- [ ] Ruff passou em lint e formatação, incluindo imports, em produção e testes.
- [ ] Testes unitários e de integração relevantes foram criados/atualizados e passaram.
- [ ] Cobertura mínima de 50% passou para o pacote de produção.
- [ ] Documentação relevante foi atualizada e `mkdocs build --strict` passou.
- [ ] `git diff --check` passou; diff foi revisado e não contém segredos ou dados sensíveis.

## Problemas comuns e soluções

- **Poetry usa outro Python:** confirme a versão exigida em `pyproject.toml`, selecione o interpretador com `poetry env use <caminho>` (ou `poetry env use "$(pyenv which python)"`) e valide com `poetry run python --version`.
- **Ambiente virtual não está no projeto:** execute `poetry config virtualenvs.in-project true --local` antes de criar o ambiente e consulte `poetry env info --path`. Se houver ambiente anterior inadequado, identifique-o primeiro e remova apenas esse ambiente com `poetry env remove <interpretador>`.
- **Dependência não está disponível no comando:** confirme que ela está no grupo correto do `pyproject.toml`, execute `poetry install` e use `poetry run <comando>`.
- **Lockfile desatualizado:** execute `poetry lock` e depois `poetry install`; revise e versione `pyproject.toml` e `poetry.lock` juntos.
- **Pacote não é encontrado:** confirme o caminho `src/<pacote>/`, o `__init__.py` quando aplicável e a configuração `packages` no Poetry; instale com `poetry install` e use o nome de importação real.
- **Ruff relata regra inesperada:** leia a regra e corrija a causa. Use `poetry run ruff check . --fix` para correções seguras; exceções requerem escopo mínimo e justificativa.
- **Cobertura abaixo de 50%:** consulte `term-missing`, confirme `source`/`--cov` e adicione testes de comportamento para caminhos não exercitados; não exclua código para contornar o limite.
- **MkDocs reporta página ou link ausente:** confira os caminhos em `nav`, crie a página necessária ou corrija o link. Não silencie avisos para fazer passar `--strict`.
- **Teste depende de serviço externo:** substitua a dependência por fixture/fake/mock na unidade testada e mova a validação real da integração para `tests/integration/`.

## Critérios de aceitação

Uma alteração ou entrega está pronta quando:

- a estrutura do projeto segue `src/` e mantém testes separados;
- Poetry gerencia dependências e ambiente, `poetry.lock` está versionado e nenhuma dependência do projeto foi instalada por `pip` ou globalmente;
- módulos têm responsabilidade clara, baixo acoplamento, alta coesão e fronteiras explícitas de infraestrutura;
- Ruff está configurado no `pyproject.toml` e passa no código de produção e nos testes, incluindo formatação e imports;
- pytest passa com testes determinísticos e pertinentes, e cobertura total de `src/projeto/` é pelo menos 50%;
- documentação utiliza MkDocs Material e `poetry run mkdocs build --strict` passa;
- CI/CD executa lint, validação de formatação, testes, limite de cobertura e build estrito da documentação;
- segredos não estão versionados; configuração e credenciais são obtidas de fontes seguras;
- código público e componentes relevantes possuem type hints e documentação adequados;
- diff, contratos, logs, impacto de performance e possibilidade de reprocessamento foram revisados.

Checklist final obrigatória:

- [ ] O projeto utiliza estrutura baseada em `src/`.
- [ ] O Poetry é utilizado para dependências e ambiente virtual.
- [ ] Nenhuma dependência foi instalada com `pip`.
- [ ] O `poetry.lock` está versionado.
- [ ] O projeto está dividido em módulos com responsabilidades claras.
- [ ] O Ruff está configurado no `pyproject.toml`.
- [ ] O Ruff verifica lint, formatação e imports.
- [ ] Os testes unitários utilizam pytest.
- [ ] A cobertura mínima de 50% é validada automaticamente.
- [ ] A documentação utiliza MkDocs Material.
- [ ] A documentação é validada com `mkdocs build --strict`.
- [ ] O CI/CD executa lint, formatação, testes, cobertura e build da documentação.
- [ ] O projeto não depende de instalações globais.
- [ ] Segredos não estão versionados.
- [ ] O código possui documentação e type hints adequados.
