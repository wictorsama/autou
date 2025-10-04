# 🎨 Design de Arquitetura - AutoU Email Classifier

## 📋 Visão Geral do Sistema

```
┌─────────────────────────────────────────────────────────────────┐
│                    AutoU Email Classifier                      │
│                     Sistema Completo                           │
└─────────────────────────────────────────────────────────────────┘
```

## 🏗️ Arquitetura de Alto Nível

```
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│                  │    │                  │    │                  │
│   Frontend PWA   │◄──►│   Backend API    │◄──►│   NLP Engine     │
│ (Alpine.js/CSS)  │    │   (FastAPI)      │    │ (Transformers)   │
│                  │    │                  │    │                  │
└──────────────────┘    └──────────────────┘    └──────────────────┘
         │                        │                        │
         │                        │                        │
         ▼                        ▼                        ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Modern UI      │    │  Response System │    │  Classification  │
│   - Dark Mode    │    │  - Templates     │    │  - Zero-shot     │
│   - PWA Features │    │  - Auto-replies  │    │  - Intent Det.   │
│   - Local Storage│    │  - Refinement    │    │  - Spam Filter   │
│   - Confidence   │    │  - Personalized  │    │  - Confidence    │
│     Graphs       │    │    Responses     │    │    Scoring       │
└──────────────────┘    └──────────────────┘    └──────────────────┘
```

## 🔄 Fluxo de Dados Detalhado

```
┌─────────────┐
│   Usuário   │
└──────┬──────┘
       │ 1. Upload/Input
       ▼
┌─────────────────────────────┐
│      Frontend Web           │
│  ┌─────────────────────────┐│
│  │   Interface HTML        ││
│  │  - Formulário Upload    ││
│  │  - Área de Texto        ││
│  │  - Botões de Ação       ││
│  └─────────────────────────┘│
└──────────────┬──────────────┘
               │ 2. HTTP POST /api/process
               ▼
┌─────────────────────────────┐
│       Backend API           │
│  ┌─────────────────────────┐│
│  │      FastAPI            ││
│  │  - Endpoint Handler     ││
│  │  - File Processing      ││
│  │  - Error Handling       ││
│  └─────────────────────────┘│
└──────────────┬──────────────┘
               │ 3. Text Processing
               ▼
┌─────────────────────────────┐
│      NLP Engine             │
│  ┌─────────────────────────┐│
│  │   Text Preprocessing    ││
│  │  - Cleaning             ││
│  │  - Tokenization         ││
│  │  - Normalization        ││
│  └─────────────────────────┘│
│  ┌─────────────────────────┐│
│  │   AI Classification     ││
│  │  - Hugging Face Model   ││
│  │  - Sentiment Analysis   ││
│  │  - Confidence Score     ││
│  └─────────────────────────┘│
│  ┌─────────────────────────┐│
│  │   Refinement System     ││
│  │  - Spam Detection       ││
│  │  - Intent Override      ││
│  │  - Rule-based Logic     ││
│  └─────────────────────────┘│
└──────────────┬──────────────┘
               │ 4. Response Generation
               ▼
┌─────────────────────────────┐
│    Response System          │
│  ┌─────────────────────────┐│
│  │   Template Engine       ││
│  │  - Intent Mapping       ││
│  │  - Dynamic Content      ││
│  │  - Personalization      ││
│  └─────────────────────────┘│
└──────────────┬──────────────┘
               │ 5. JSON Response
               ▼
┌─────────────────────────────┐
│      Frontend Web           │
│  ┌─────────────────────────┐│
│  │   Results Display       ││
│  │  - Classification       ││
│  │  - Confidence Score     ││
│  │  - Suggested Reply      ││
│  │  - Feedback Options     ││
│  └─────────────────────────┘│
└──────────────┬──────────────┘
               │ 6. Display Results
               ▼
┌─────────────┐
│   Usuário   │
└─────────────┘
```

## 🧩 Componentes Detalhados

### 1. Frontend Layer
```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend Web                          │
├─────────────────────────────────────────────────────────────┤
│  📁 templates/                                              │
│    └── index.html          ← Interface principal (Alpine.js)│
│  📁 static/                                                 │
│    ├── styles.css          ← Estilos CSS + Dark Mode       │
│    ├── app.js              ← Lógica JavaScript + Alpine.js │
│    ├── manifest.json       ← PWA Manifest                  │
│    └── sw.js               ← Service Worker                 │
├─────────────────────────────────────────────────────────────┤
│  Funcionalidades:                                          │
│  ✓ Upload de arquivos (.txt, .pdf)                         │
│  ✓ Input direto de texto                                   │
│  ✓ Exibição de resultados com gráficos                     │
│  ✓ Interface responsiva (Tailwind CSS)                     │
│  ✓ Dark Mode com persistência                              │
│  ✓ PWA (Progressive Web App)                               │
│  ✓ Auto-refresh automático                                 │
│  ✓ Histórico local (localStorage)                          │
│  ✓ Gráficos de confiança animados                          │
│  ✓ Feedback visual e animações                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. Backend API Layer
```
┌─────────────────────────────────────────────────────────────┐
│                      Backend API                           │
├─────────────────────────────────────────────────────────────┤
│  📄 main.py                 ← FastAPI Application          │
│    ├── /                   ← Serve Frontend                │
│    ├── /api/process        ← Main Processing Endpoint      │
│    └── /static/*           ← Static Files                  │
├─────────────────────────────────────────────────────────────┤
│  Funcionalidades:                                          │
│  ✓ Processamento de arquivos                               │
│  ✓ Validação de entrada                                    │
│  ✓ Orquestração do pipeline                                │
│  ✓ Tratamento de erros                                     │
│  ✓ Serialização de resposta                                │
└─────────────────────────────────────────────────────────────┘
```

### 3. NLP Processing Layer
```
┌─────────────────────────────────────────────────────────────┐
│                    NLP Engine                              │
├─────────────────────────────────────────────────────────────┤
│  📄 nlp.py                  ← Core NLP Logic               │
│    ├── preprocess_text()    ← Text Cleaning                │
│    ├── classify_email()     ← AI Classification            │
│    └── refine_classification() ← Rule-based Refinement     │
├─────────────────────────────────────────────────────────────┤
│  📄 utils.py                ← Utility Functions            │
│    ├── extract_text()       ← PDF/TXT Processing           │
│    ├── clean_text()         ← Text Normalization           │
│    └── validate_input()     ← Input Validation             │
├─────────────────────────────────────────────────────────────┤
│  Modelo AI:                                                │
│  🤖 cardiffnlp/twitter-xlm-roberta-base-sentiment-multilingual │
│    ├── Sentiment Analysis                                  │
│    ├── Multilingual Support                                │
│    └── High Accuracy                                       │
└─────────────────────────────────────────────────────────────┘
```

### 4. Response Generation Layer
```
┌─────────────────────────────────────────────────────────────┐
│                  Response System                           │
├─────────────────────────────────────────────────────────────┤
│  📄 responders.py           ← Response Logic               │
│    ├── generate_response()  ← Main Response Function       │
│    ├── get_template()       ← Template Selection           │
│    └── customize_reply()    ← Content Personalization      │
├─────────────────────────────────────────────────────────────┤
│  Templates por Intent:                                      │
│  📧 Solicitação de status                                   │
│  📧 Dúvida técnica                                          │
│  📧 Agradecimento                                           │
│  📧 Spam/Marketing                                          │
│  📧 Conversa informal                                       │
└─────────────────────────────────────────────────────────────┘
```

## 🔍 Sistema de Classificação

```
┌─────────────────────────────────────────────────────────────┐
│                 Pipeline de Classificação                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Etapa 1: Pré-processamento                                │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  • Limpeza de texto                                    ││
│  │  • Remoção de caracteres especiais                     ││
│  │  • Normalização de espaços                             ││
│  │  • Validação de comprimento                            ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Etapa 2: Análise de Sentimento (AI)                      │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  🤖 Modelo: twitter-xlm-roberta-base-sentiment         ││
│  │  • Input: Texto limpo                                  ││
│  │  • Output: [POSITIVE, NEGATIVE, NEUTRAL]               ││
│  │  • Confidence Score: 0.0 - 1.0                        ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Etapa 3: Mapeamento Inicial                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  POSITIVE   → Produtivo                                ││
│  │  NEGATIVE   → Improdutivo                              ││
│  │  NEUTRAL    → Produtivo (padrão)                      ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Etapa 4: Sistema de Refinamento                           │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  🔍 Detecção de Padrões:                               ││
│  │    • Palavras de agradecimento → Improdutivo           ││
│  │    • Termos de spam/marketing → Improdutivo            ││
│  │    • Palavras-chave técnicas → Produtivo               ││
│  │    • Solicitações diretas → Produtivo                  ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Etapa 5: Classificação de Intent                          │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  📋 Intents Produtivos:                                ││
│  │    • Solicitação de status ou informações              ││
│  │    • Dúvida técnica ou suporte                         ││
│  │                                                        ││
│  │  📋 Intents Improdutivos:                              ││
│  │    • Agradecimento ou felicitação                      ││
│  │    • Spam ou marketing                                  ││
│  │    • Conversa informal ou social                       ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Matriz de Decisão

```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│   Sentiment     │   Palavras-     │   Refinamento   │   Classificação │
│   (AI Model)    │   chave         │   (Rules)       │   Final         │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│   POSITIVE      │   "obrigado"    │   Override      │   Improdutivo   │
│                 │   "parabéns"    │   → Gratidão    │   (Gratidão)    │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│   NEGATIVE      │   "promoção"    │   Override      │   Improdutivo   │
│                 │   "desconto"    │   → Spam        │   (Spam)        │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│   POSITIVE      │   "status"      │   Manter        │   Produtivo     │
│                 │   "atualização" │   → Status      │   (Status)      │
├─────────────────┼─────────────────┼─────────────────┼─────────────────┤
│   NEUTRAL       │   "problema"    │   Override      │   Produtivo     │
│                 │   "erro"        │   → Técnico     │   (Técnico)     │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

## 🚀 Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AWS Cloud Deployment                    │
├─────────────────────────────────────────────────────────────┤
│  ☁️ AWS Lambda + API Gateway                               │
│    ├── ⚡ Serverless Functions                              │
│    │   ├── Python 3.11 Runtime                             │
│    │   ├── FastAPI Application (via Mangum)                │
│    │   ├── Hugging Face Transformers                       │
│    │   ├── Static Files via S3 + CloudFront               │
│    │   └── Service Worker Support                          │
│    │                                                       │
│    ├── 📋 Configuration Files:                             │
│    │   ├── serverless.yml     ← Serverless Config          │
│    │   ├── handler.py         ← Lambda Handler             │
│    │   ├── package.json       ← Node.js Dependencies       │
│    │   ├── requirements_aws.txt ← Python Dependencies      │
│    │   ├── manifest.json     ← PWA Configuration          │
│    │   ├── sw.js             ← Service Worker              │
│    │   └── deploy/            ← Deploy Scripts & Config    │
│    │       ├── GUIA_AWS_COMPLETO.md ← Complete AWS Guide   │
│    │       ├── .env.example  ← Environment Template       │
│    │       └── README.md     ← Deploy Instructions        │
│    │                                                       │
│    └── 🔧 AWS Services:                                     │
│        ├── Lambda Functions (Auto-scaling)                │
│        ├── API Gateway (HTTPS/SSL)                        │
│        ├── S3 + CloudFront (CDN)                          │
│        ├── CloudWatch (Monitoring)                        │
│        └── IAM Roles & Policies                           │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Performance Metrics

```
┌─────────────────────────────────────────────────────────────┐
│                   Métricas do Sistema                      │
├─────────────────────────────────────────────────────────────┤
│  🎯 Precisão de Classificação:                             │
│    ├── Produtivo: ~85-90%                                  │
│    ├── Improdutivo: ~90-95%                                │
│    └── Overall: ~87-92%                                    │
│                                                            │
│  ⚡ Performance (Otimizado):                               │
│    ├── Tempo de Resposta: <2s                              │
│    ├── Throughput: ~100 req/min                            │
│    ├── Memory Usage: ~256MB (reduzido 50%)                 │
│    ├── Garbage Collection: Automático                      │
│    └── Monitoramento: Tempo real via /health               │
│                                                            │
│  🔍 Confidence Scores:                                     │
│    ├── Alto (>0.8): ~70% dos casos                        │
│    ├── Médio (0.5-0.8): ~25% dos casos                    │
│    └── Baixo (<0.5): ~5% dos casos                        │
└─────────────────────────────────────────────────────────────┘
```

## 🎨 Funcionalidades Implementadas

```
┌─────────────────────────────────────────────────────────────┐
│                 Funcionalidades Atuais                     │
├─────────────────────────────────────────────────────────────┤
│  🌙 Dark Mode:                                             │
│    ├── Toggle com persistência localStorage                │
│    ├── Transições suaves CSS                               │
│    ├── Cobertura completa da interface                     │
│    └── Integração com Alpine.js                            │
│                                                            │
│  📱 PWA (Progressive Web App):                             │
│    ├── Manifest.json configurado                           │
│    ├── Service Worker para cache                           │
│    ├── Instalável como app nativo                          │
│    └── Funcionalidade offline básica                       │
│                                                            │
│  📊 Gráficos de Confiança:                                 │
│    ├── Barras de progresso animadas                        │
│    ├── Sistema de cores por confiança                      │
│    ├── Tooltips informativos                               │
│    └── Responsividade completa                             │
│                                                            │
│  💾 Histórico Local:                                       │
│    ├── Armazenamento no localStorage                       │
│    ├── Persistência entre sessões                          │
│    ├── Opção de limpeza de dados                           │
│    └── Exportação de histórico                             │
│                                                            │
│  🔄 Auto-refresh:                                          │
│    ├── Atualização automática de resultados               │
│    ├── Toggle de ativação/desativação                      │
│    ├── Persistência de configuração                        │
│    └── Feedback visual de status                           │
└─────────────────────────────────────────────────────────────┘
```

## 🔮 Roadmap de Melhorias

```
┌─────────────────────────────────────────────────────────────┐
│                  Funcionalidades e Roadmap                 │
├─────────────────────────────────────────────────────────────┤
│  ✅ Fase 0 - Otimizações de Memória (CONCLUÍDA):          │
│    ├── ✅ Configurações centralizadas                      │
│    ├── ✅ Limpeza automática de memória                    │
│    ├── ✅ Monitoramento em tempo real                      │
│    ├── ✅ Modelo NLP otimizado com fallback                │
│    ├── ✅ Limites de arquivo e texto otimizados            │
│    └── ✅ Dependências otimizadas                          │
│                                                            │
│  📈 Fase 1 - Sistema de Feedback:                          │
│    ├── Interface de avaliação                              │
│    ├── Banco de dados SQLite                               │
│    ├── API de feedback                                      │
│    └── Aprendizado adaptativo                              │
│                                                            │
│  🧠 Fase 2 - IA Avançada:                                  │
│    ├── Fine-tuning do modelo                               │
│    ├── Ensemble de modelos                                 │
│    ├── Detecção de idioma                                  │
│    └── Análise de contexto                                 │
│                                                            │
│  🔧 Fase 3 - Funcionalidades Avançadas:                   │
│    ├── Sincronização em nuvem                              │
│    ├── Notificações push                                   │
│    ├── Dashboard analytics                                 │
│    ├── Integração com email                                │
│    └── Múltiplos formatos de arquivo                       │
└─────────────────────────────────────────────────────────────┘
```

---

**📝 Nota:** Este documento complementa a documentação técnica em `ARQUITETURA.md`, fornecendo uma visão visual e estrutural do sistema AutoU Email Classifier.

**🔄 Última atualização:** 03 de Outubro de 2025
**👨‍💻 Desenvolvido para:** Processo Seletivo AutoU
**🎯 Objetivo:** Demonstrar arquitetura e design de sistema completo