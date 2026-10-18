# Próximos passos

Esta página separa o que já existe no MVP do que ainda não está implementado.
Os itens futuros refletem o escopo declarado para o projeto; não indicam
prioridade, prazo ou compromisso de entrega.

## Já disponível

- Biblioteca Python para consultar `/meetings`, `/sessions`, `/drivers` e
  `/laps` da OpenF1.
- Dashboard Streamlit para escolher temporada, Grand Prix e sessão, e visualizar
  até cinco voltas mais rápidas e os pilotos daquela sessão.
- Tratamento explícito de erros de rede, HTTP e formato de resposta.
- Testes unitários sem dependência de chamadas reais à API.

## Fora do MVP; possíveis evoluções

- **Mais dados de corrida:** adicionar operações de serviço para outros
  endpoints da OpenF1, como dados de telemetria, após definir os campos e o
  comportamento que a interface precisa.
- **Modelos de domínio:** substituir ou complementar os dicionários genéricos
  com tipos próprios quando contratos estáveis e regras de negócio adicionais
  justificarem essa camada.
- **Dashboard:** expandir os dados e visualizações além das voltas mais rápidas
  e da tabela de pilotos, guiado por casos de uso definidos.
- **Acesso em tempo real:** avaliar suporte separado dos dados históricos,
  incluindo autenticação e requisitos próprios da API.
- **CLI:** oferecer consultas por terminal se houver necessidade de uso sem a
  interface gráfica.
- **Persistência/cache:** avaliar armazenamento local ou cache somente se
  requisitos de desempenho, histórico ou funcionamento offline forem
  estabelecidos.

Antes de iniciar uma dessas evoluções, defina o contrato esperado, atualize os
testes para cobrir o comportamento sem depender da rede e documente as
consequências para a API pública e para o dashboard.
