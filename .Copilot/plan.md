# Plano de criação do projeto F1

## Problema e abordagem

O repositório continha apenas o esqueleto do pacote `f1`, sem funcionalidades,
testes ou documentação operacional. Este plano estabelece uma primeira versão
utilizável para consultar dados históricos da OpenF1, seguindo os padrões de
engenharia definidos em [`.Copilot/SKILL.md`](.Copilot/SKILL.md) e os endpoints
descritos em [`.Copilot/doc_api.md`](.Copilot/doc_api.md).

O MVP é uma biblioteca Python para consultar meetings, sessions e dados de
pilotos associados a uma sessão. A comunicação usa `urllib` da biblioteca
padrão; os resultados são devolvidos como dados JSON/Python, sem persistência
externa. Telemetria, os demais endpoints, CLI e armazenamento ficam para fases
futuras.

## Escopo do MVP

- Configurar dependências, empacotamento, Ruff, pytest e cobertura no Poetry,
  preservando o pacote `f1` e `requires-python >=3.12`.
- Criar um cliente OpenF1 pequeno e reutilizável, isolando a chamada HTTP e a
  construção de URLs/parâmetros.
- Expor operações para listar meetings por temporada, listar sessions de um
  meeting/temporada e consultar pilotos por sessão.
- Permitir filtros combinados por meio de parâmetros explícitos.
- Aplicar timeout e tratamento explícito de falhas HTTP, rede, decodificação JSON
  e resposta inválida; não mascarar falhas com resultados vazios.
- Testar regras sem rede real com mocks/fakes na fronteira HTTP.
- Documentar instalação, configuração e exemplos de uso em português, com
  MkDocs Material e build estrito.
- Adicionar CI para lint, verificação de formatação, testes/cobertura e build da
  documentação.

## Fases

1. **Preparar a base:** configurar Poetry, lockfile, Ruff, pytest, cobertura,
   `.gitignore` e empacotamento do pacote `f1`.
2. **Implementar acesso OpenF1:** criar cliente baseado em `urllib`, contratos
   tipados e serviços para meetings, sessions e drivers.
3. **Adicionar testes:** cobrir parâmetros, contratos, respostas e erros sem
   depender de rede, com cobertura mínima de 50%.
4. **Documentar e automatizar:** criar README, documentação MkDocs Material e
   workflow de CI com as validações exigidas.
5. **Validar a entrega:** executar instalação, lint, formatação, testes com
   cobertura, build estrito da documentação e revisão do diff.

## Componentes previstos

- `src/f1/clients/`: cliente HTTP OpenF1 e tratamento de transporte.
- `src/f1/services/`: operações de meetings, sessions e drivers.
- `tests/unit/`: testes unitários isolados da rede.
- `docs/`, `mkdocs.yml`, `README.md`: documentação de uso e operação.
- `.github/workflows/`: validações contínuas do projeto.

Os módulos e diretórios devem ser criados apenas quando necessários, mantendo
uma solução pequena e sem abstrações de persistência/orquestração ainda não
utilizadas.

## Decisões e considerações

- **Interface:** biblioteca Python; CLI fica fora do MVP.
- **Endpoints:** `/meetings`, `/sessions` e `/drivers`; telemetria e os demais
  recursos ficam para fases futuras.
- **Transporte:** `urllib`, sem dependência de produção adicional.
- **Saída:** estruturas Python decodificadas do JSON; sem banco, arquivos, cache
  ou exportação no MVP.
- **Autenticação:** não necessária para os dados históricos descritos na
  documentação OpenF1; dados em tempo real ficam fora do escopo.
- **Contratos:** modelar somente os campos usados, aceitando campos opcionais e
  sem presumir schema mais amplo que a API confirme.
- **Qualidade:** Poetry para dependências/ambiente; Ruff; pytest com cobertura
  global mínima de 50%; MkDocs Material em modo estrito.
- **CI:** GitHub Actions, sujeito à confirmação de que não há workflow existente
  a reutilizar.
- **Segurança:** não versionar credenciais, dados pessoais ou arquivos locais
  sensíveis; não instalar dependências do projeto com `pip`.
