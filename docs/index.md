# F1 — dados da OpenF1

O pacote `f1` consulta dados históricos da [OpenF1](https://openf1.org/), API
que disponibiliza informações de meetings, sessions, pilotos e dados de corrida
da Fórmula 1.

O MVP oferece uma biblioteca Python para consultar meetings por temporada,
sessions, pilotos e voltas de uma sessão. Inclui também um dashboard Streamlit
para explorar meetings, sessões e as cinco voltas mais rápidas. Utiliza `urllib`
da biblioteca padrão, não exige autenticação para os dados históricos e não
persiste respostas.

## Escopo atual

- Consultas aos endpoints `/meetings`, `/sessions`, `/drivers` e `/laps`.
- Resultados como listas de dicionários Python.
- Dashboard para selecionar temporada, Grand Prix e sessão, visualizar voltas
  mais rápidas e consultar os pilotos.
- Falhas de rede, HTTP e respostas inválidas representadas por exceções
  específicas do pacote.

Telemetria, demais endpoints, acesso em tempo real, CLI e armazenamento ainda
não fazem parte do MVP. Consulte [próximos passos](roadmap.md) para o que está
fora do escopo atual.

## Comece aqui

- [Instalação](installation.md)
- [Uso da biblioteca](usage.md)
- [Arquitetura e camadas](architecture.md)
- [Desenvolvimento e testes](development.md)
- [Referência da API Python](api/index.md)
- [Próximos passos](roadmap.md)
