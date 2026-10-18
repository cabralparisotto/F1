# Arquitetura e camadas

O projeto usa a estrutura `src/` e separa a interface, as operações de consulta
e a comunicação HTTP. As camadas são responsabilidades lógicas; ainda não há
um pacote ou uma pasta chamada `domain`:

```text
src/f1/
├── dashboard.py
├── clients/
│   └── openf1.py
├── services/
│   └── openf1.py
├── laps.py
├── errors.py
└── __init__.py
```

- **Apresentação (`dashboard.py`)**: interface Streamlit. Carrega a temporada,
  oferece seletores de Grand Prix e sessão, apresenta mensagens de erro e exibe
  tabelas de voltas e pilotos. A interface coordena os serviços, mas não monta
  URLs nem faz chamadas HTTP diretamente.
- **Serviços (`services/openf1.py`)**: `OpenF1Service` oferece consultas para
  meetings, sessions, drivers e laps. Combina filtros e rejeita chaves
  duplicadas antes de encaminhar a consulta ao cliente.
- **Cliente/infraestrutura (`clients/openf1.py`)**: `OpenF1Client` valida a URL
  e o timeout, codifica parâmetros de query, executa GET com `urllib`, decodifica
  JSON e valida a estrutura dos registros.
- **Lógica de domínio (`laps.py`)**: `fastest_laps` filtra voltas com duração
  positiva, ordena por tempo, limita o resultado a cinco e associa números de
  piloto a nomes. É uma função independente de Streamlit e da rede. O projeto
  ainda usa os dicionários da API diretamente; não possui entidades ou modelos
  de domínio dedicados.
- **Erros (`errors.py`)**: define a exceção base e diferencia falhas de
  transporte, status HTTP e conteúdo de resposta inválido.
- **API pública (`__init__.py`)**: expõe cliente, serviço e exceções como
  `f1.OpenF1Service`.

O serviço aceita um cliente por injeção, permitindo testar o encaminhamento de
filtros sem rede. O cliente usa um timeout finito e propaga falhas como exceções
`OpenF1Error`, sem retornar uma resposta vazia como se a consulta tivesse sido
bem-sucedida.

## Fluxo de dados

1. O dashboard chama `OpenF1Service` com as chaves da temporada, meeting ou
   sessão selecionada.
2. O serviço combina os filtros e os encaminha ao cliente.
3. O cliente consulta a OpenF1 e valida que a resposta é uma lista JSON de
   objetos.
4. Para a tabela de voltas, `fastest_laps` transforma registros brutos em até
   cinco resultados apresentados pelo dashboard.
5. O dashboard mostra os dados ou informa explicitamente a falha ao usuário.

Não há banco, persistência, cache, autenticação ou acesso em tempo real. A
transformação de domínio existente limita-se à classificação das voltas; os
demais dados continuam como registros retornados pela API.
