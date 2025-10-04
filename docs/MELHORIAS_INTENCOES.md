# Melhorias nas Intenções de Email - AutoU

## 📋 Resumo das Melhorias

Implementamos intenções mais específicas e convencionais para classificação de emails corporativos, expandindo de 6 para 16 tipos de intenção diferentes.

## 🎯 Novas Intenções Implementadas

### Emails Produtivos (Requerem Ação)

1. **Solicitação de status ou acompanhamento**
   - Palavras-chave: status, andamento, situação, acompanhamento, posição
   - Exemplo: "Preciso do status do chamado #12345"

2. **Pedido de informações ou esclarecimentos**
   - Para solicitações gerais de informação
   - Exemplo: "Gostaria de saber mais sobre o processo de contratação"

3. **Envio de documentos ou arquivos importantes**
   - Mantido da versão anterior, mas com nome mais específico
   - Exemplo: "Segue anexo o contrato assinado"

4. **Dúvida técnica ou solicitação de suporte**
   - Mantido da versão anterior com nome atualizado
   - Exemplo: "Estou com problema no sistema, não consigo acessar"

5. **Agendamento de reunião ou compromisso**
   - Palavras-chave: reunião, meeting, agendar, marcar, disponibilidade, horário
   - Exemplo: "Podemos agendar uma reunião para discutir o projeto?"

6. **Aprovação ou autorização necessária**
   - Palavras-chave: aprovar, aprovação, autorizar, autorização, validar
   - Exemplo: "Preciso da sua aprovação para prosseguir com a compra"

7. **Cobrança ou follow-up de pendências**
   - Palavras-chave: cobrança, pendência, follow-up, prazo, vencimento
   - Exemplo: "Seguindo nosso último contato sobre o pagamento em atraso"

8. **Solicitação de orçamento ou proposta**
   - Palavras-chave: orçamento, proposta, cotação, preço, valor, custo
   - Exemplo: "Gostaria de solicitar um orçamento para o serviço X"

### Emails Improdutivos (Informativos ou Sociais)

9. **Agradecimento ou felicitação**
   - Mantido da versão anterior
   - Exemplo: "Obrigado pelo excelente atendimento!"

10. **Confirmação ou comunicado informativo**
    - Para emails apenas informativos
    - Exemplo: "Informamos que o sistema estará em manutenção amanhã"

11. **Conversa informal ou social**
    - Mantido da versão anterior
    - Exemplo: "Como foi o final de semana?"

12. **Spam ou marketing**
    - Mantido da versão anterior
    - Exemplo: "OFERTA IMPERDÍVEL! 70% DE DESCONTO!"

13. **Notificação automática do sistema**
    - Palavras-chave: notificação, automático, sistema, noreply, no-reply
    - Exemplo: "Sua senha expirará em 7 dias"

14. **Convite para evento ou treinamento**
    - Palavras-chave: convite, evento, treinamento, curso, workshop, palestra
    - Exemplo: "Convite para o workshop de inovação"

## 🧠 Lógica de Classificação Inteligente

### Detecção por Palavras-Chave
Implementamos um sistema de detecção baseado em palavras-chave específicas que sobrescreve a classificação do modelo de IA quando necessário, garantindo maior precisão.

### Priorização de Contexto
A lógica segue uma ordem de prioridade:
1. Detecção por palavras-chave específicas
2. Classificação do modelo de IA (XLM-RoBERTa)
3. Refinamentos baseados em padrões (spam, agradecimentos)

## 📝 Templates de Resposta

Cada nova intenção possui um template de resposta específico e profissional:

- **Linguagem formal corporativa** em português brasileiro
- **Campos dinâmicos** como {nome}, {sla}, {referencia}
- **Contexto apropriado** para cada tipo de solicitação
- **Call-to-action** quando necessário

## 🎯 Benefícios das Melhorias

1. **Maior Precisão**: Classificação mais específica e contextual
2. **Melhor UX**: Respostas mais adequadas ao tipo de solicitação
3. **Automação Inteligente**: Detecção automática de padrões comuns
4. **Escalabilidade**: Fácil adição de novas intenções e palavras-chave
5. **Profissionalismo**: Templates corporativos padronizados

## 🔧 Implementação Técnica

### Arquivos Modificados:
- `app/nlp.py`: Novas intenções e lógica de detecção
- `app/responders.py`: Templates expandidos para todas as intenções

### Compatibilidade:
- Mantém compatibilidade com a API existente
- Não quebra funcionalidades anteriores
- Melhora a precisão sem impactar performance

## 📊 Casos de Uso Cobertos

As novas intenções cobrem os principais cenários de email corporativo:
- ✅ Solicitações de status e acompanhamento
- ✅ Agendamentos e reuniões
- ✅ Aprovações e autorizações
- ✅ Orçamentos e propostas comerciais
- ✅ Follow-ups e cobranças
- ✅ Comunicados e notificações
- ✅ Eventos e treinamentos

---