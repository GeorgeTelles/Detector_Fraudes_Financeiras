# Sistema de Detecção de Fraudes em Tempo Real  
Sistema de monitoramento de transações financeiras desenvolvido para identificar atividades suspeitas e potenciais fraudes em tempo real. Utilizando análise comportamental e regras de anomalia, o sistema avalia padrões de transações para gerar alertas imediatos, facilitando uma resposta rápida a possíveis riscos.

---

## Principais Funcionalidades  
1. **Perfil Comportamental de Usuários**  
   - Cria perfis dinâmicos com base no histórico de transações, incluindo:  
     - Valor médio gasto  
     - Localização e dispositivo mais frequentes  
     - Frequência de transações  
     - Horário habitual de atividade  

2. **Critérios de Detecção de Anomalias**  
   - **Valor Atípico:** Transações acima de 3x a média histórica do usuário.  
   - **Mudança Geográfica:** Transações originadas de país diferente do padrão.  
   - **Dispositivo Incomum:** Uso de dispositivo não associado ao perfil.  
   - **Horário Suspeito:** Operações entre 00h e 05h (período de baixa atividade).  
   - **Categorias de Risco:** Transações em categorias sensíveis (ex: Viagens, Eletrônicos).  

3. **Simulação de Tempo Real**  
   - Processamento sequencial de transações com atraso configurável para simular um fluxo realista.  
   - Atualização contínua dos perfis dos usuários conforme novas transações são processadas.  

4. **Sistema de Alertas Visual**  
   - Notificações coloridas no terminal (via `colorama`) destacando:  
     - Detalhes da transação suspeita  
     - Motivos do alerta  
     - Contagem progressiva de alertas  

---

## Tecnologias e Bibliotecas  
- **Pandas:** Processamento e análise dos dados de transações.  
- **Colorama:** Geração de alertas coloridos para melhor visualização.  
- **Datetime:** Manipulação de timestamps e detecção de horários incomuns.  
- **Estrutura Orientada a Objetos:** Organização modular do código para escalabilidade.  

---

## Fluxo de Trabalho  
1. **Entrada de Dados:**  
   - Carrega transações de um arquivo Excel (`transacoes.xlsx`).  
   - Ordena transações cronologicamente para simular um fluxo realista.  

2. **Atualização de Perfis:**  
   - Mantém um dicionário de perfis de usuários, atualizando métricas a cada transação.  

3. **Verificação de Anomalias:**  
   - Aplica regras pré-definidas para cada nova transação.  
   - Combina múltiplos critérios para aumentar a precisão dos alertas.  

4. **Saída de Alertas:**  
   - Exibe detalhes da transação e razões da suspeita em destaque vermelho.  
   - Fornece estatísticas periódicas de progresso (transações analisadas/alertas).  

---

## Aplicações Práticas  
- **Prevenção de Fraudes:** Identificação proativa de transações incomuns.  
- **Monitoramento de Contas:** Detecção de comprometimento de contas (ex: acesso por dispositivos não autorizados).  
- **Análise de Risco:** Classificação de transações sensíveis para revisão manual.  
