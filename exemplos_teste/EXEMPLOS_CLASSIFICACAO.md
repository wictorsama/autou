# Exemplos de Teste - Melhorias nas Intenções

## 📋 Como Testar

1. **Acesse a aplicação**: http://localhost:8000/
2. **Cole os exemplos** na caixa de texto
3. **Observe a classificação** automática (auto-refresh) ou clique "Classificar & Sugerir"
4. **Compare os resultados** com as intenções esperadas abaixo

## 🎯 Exemplos de Emails Produtivos

### 1. Solicitação de Status (`exemplo_status.txt`)
**Texto:**
```
Bom dia,

Preciso do status do chamado #12345. Quando será resolvido?
Já faz uma semana que abri a solicitação.

Obrigado.
```
**Classificação Esperada:**
- **Categoria:** Produtivo
- **Intenção:** Solicitação de status ou acompanhamento
- **Palavras-chave detectadas:** "status", "chamado"

### 2. Agendamento de Reunião (`exemplo_reuniao.txt`)
**Texto:**
```
Olá,

Gostaria de agendar uma reunião para discutir o projeto X.
Vocês têm disponibilidade na próxima semana?
Podemos marcar para terça ou quarta-feira?

Aguardo retorno.
```
**Classificação Esperada:**
- **Categoria:** Produtivo
- **Intenção:** Agendamento de reunião ou compromisso
- **Palavras-chave detectadas:** "agendar", "reunião", "marcar", "disponibilidade"

### 3. Aprovação Necessária (`exemplo_aprovacao.txt`)
**Texto:**
```
Prezados,

Preciso da aprovação para prosseguir com a compra dos equipamentos.
O orçamento já foi validado pelo setor financeiro.
Por favor, autorizar o processo de aquisição.

Atenciosamente.
```
**Classificação Esperada:**
- **Categoria:** Produtivo
- **Intenção:** Aprovação ou autorização necessária
- **Palavras-chave detectadas:** "aprovação", "autorizar"

### 4. Solicitação de Orçamento (`exemplo_orcamento.txt`)
**Texto:**
```
Prezados,

Gostaria de solicitar um orçamento para o desenvolvimento de um sistema web.
Precisamos de uma plataforma com as seguintes funcionalidades:
- Cadastro de usuários
- Dashboard administrativo
- Relatórios gerenciais

Por favor, enviem proposta com prazo e valor.

Obrigado.
```
**Classificação Esperada:**
- **Categoria:** Produtivo
- **Intenção:** Solicitação de orçamento ou proposta
- **Palavras-chave detectadas:** "orçamento", "proposta", "valor"

## 🎯 Exemplos de Emails Improdutivos

### 5. Convite para Evento (`exemplo_convite.txt`)
**Texto:**
```
Olá pessoal,

Convite para o workshop de inovação que acontecerá na próxima sexta-feira.
O evento será das 14h às 17h no auditório principal.
Haverá coffee break e certificado de participação.

Esperamos vocês lá!
```
**Classificação Esperada:**
- **Categoria:** Improdutivo
- **Intenção:** Convite para evento ou treinamento
- **Palavras-chave detectadas:** "convite", "workshop", "evento"

### 6. Notificação Automática (`exemplo_notificacao.txt`)
**Texto:**
```
Notificação Automática do Sistema

Sua senha expirará em 7 dias.
Para renovar, acesse: sistema.empresa.com/senha

Esta é uma mensagem automática, não responda.
noreply@empresa.com
```
**Classificação Esperada:**
- **Categoria:** Improdutivo
- **Intenção:** Notificação automática do sistema
- **Palavras-chave detectadas:** "notificação", "automática", "noreply"

## 🧠 O que Observar

### ✅ Melhorias Implementadas:
1. **Detecção Inteligente**: Palavras-chave específicas sobrescrevem a IA quando necessário
2. **Intenções Específicas**: 16 tipos diferentes vs. 6 anteriores
3. **Templates Contextuais**: Respostas adequadas para cada tipo de solicitação
4. **Classificação Híbrida**: Combina IA + regras + contexto

### 📊 Comparação com Versão Anterior:
- **Antes**: "Solicitação de status ou informações" (genérico)
- **Agora**: "Solicitação de status ou acompanhamento" (específico)
- **Antes**: 6 intenções básicas
- **Agora**: 16 intenções detalhadas

## 🎯 Teste Adicional

Experimente misturar palavras-chave de diferentes intenções para ver como o sistema prioriza:

```
Preciso agendar uma reunião para discutir a aprovação do orçamento.
Qual o status da proposta que enviamos?
```

O sistema deve detectar múltiplas intenções e escolher a mais relevante baseada no contexto.

---

**Dica**: Use o modo escuro/claro para testar a interface em diferentes condições visuais!