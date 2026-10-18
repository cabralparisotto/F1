# Contribuição

1. Crie uma branch focada na mudança.
2. Implemente em módulos pequenos, mantendo produção em `src/` e testes em
   `tests/`.
3. Atualize os testes e a documentação quando o comportamento ou a interface
   mudar.
4. Execute lint, formatação, cobertura e build estrito:

   ```bash
   poetry run ruff check .
   poetry run ruff format --check .
   poetry run pytest --cov=f1 --cov-report=term-missing --cov-fail-under=50
   poetry run mkdocs build --strict
   ```

5. Revise o diff, `poetry.lock` quando aplicável, e confirme que não incluiu
   segredos, dados reais sensíveis ou arquivos de ambiente locais.

Dependências devem ser gerenciadas pelo Poetry. Não enfraqueça asserts ou
desative regras para fazer as verificações passarem sem justificar a alteração.
