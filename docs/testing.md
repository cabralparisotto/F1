# Testes

Execute a suíte unitária e valide a cobertura mínima de 50% do pacote:

```bash
poetry run pytest --cov=f1 --cov-report=term-missing --cov-fail-under=50
```

Os testes em `tests/unit/` cobrem construção da query string, filtros repetidos,
respostas JSON válidas/inválidas, falhas HTTP/transporte e encaminhamento de
filtros pelos serviços. A fronteira de rede é substituída por mocks e respostas
controladas: a suíte padrão não depende da disponibilidade da OpenF1.

Testes que dependam de rede real são opcionais e não devem ser necessários para
validar mudanças locais ou CI.
