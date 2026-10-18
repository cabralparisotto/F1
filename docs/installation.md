# Instalação

## Requisitos

- Python 3.12 ou superior
- Poetry 2.x

O Poetry gerencia o ambiente virtual, dependências e lockfile do projeto.
Instale-o por um método oficial aprovado para o seu sistema operacional.

## Instalar o projeto

Na raiz do repositório:

```bash
poetry install
```

O comando instala as dependências de desenvolvimento declaradas e o pacote `f1`
no ambiente virtual do projeto. O projeto não exige dependências de produção
adicionais para chamadas HTTP.

## Verificar a instalação

```bash
poetry run python --version
poetry run python -c "from f1 import OpenF1Service; print(OpenF1Service)"
```
