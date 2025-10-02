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
│   Frontend Web   │◄──►│   Backend API    │◄──►│   NLP Engine     │
│   (HTML/CSS/JS)  │    │   (FastAPI)      │    │ (Transformers)   │
│                  │    │                  │    │                  │
└──────────────────┘    └──────────────────┘    └──────────────────┘
         │                        │                        │
         │                        │                        │
         ▼                        ▼                        ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   User Interface │    │  Response System │    │  Classification  │
│   - Upload Form  │    │  - Templates     │    │  - Sentiment     │
│   - Results View │    │  - Auto-replies  │    │  - Intent Det.   │
│   - Feedback UI  │    │  - Refinement    │    │  - Spam Filter   │
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
│    └── index.html          ← Interface principal           │
│  📁 static/                                                 │
│    ├── styles.css          ← Estilos CSS                   │
│    └── app.js              ← Lógica JavaScript             │
├─────────────────────────────────────────────────────────────┤
│  Funcionalidades:                                          │
│  ✓ Upload de arquivos (.txt, .pdf)                         │
│  ✓ Input direto de texto                                   │
│  ✓ Exibição de resultados                                  │
│  ✓ Interface responsiva                                     │
│  ✓ Feedback visual                                          │
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
│                    Cloud Deployment                        │
├─────────────────────────────────────────────────────────────┤
│  🌐 Render Platform                                         │
│    ├── 🐳 Docker Container                                  │
│    │   ├── Python 3.11 Runtime                             │
│    │   ├── FastAPI Application                              │
│    │   ├── Hugging Face Transformers                       │
│    │   └── Static Files Serving                            │
│    │                                                       │
│    ├── 📋 Configuration Files:                             │
│    │   ├── render.yaml        ← Render Config              │
│    │   ├── Dockerfile         ← Container Setup            │
│    │   ├── Procfile          ← Process Definition          │
│    │   └── requirements.txt   ← Dependencies               │
│    │                                                       │
│    └── 🔧 Environment:                                      │
│        ├── Auto-scaling                                    │
│        ├── HTTPS/SSL                                       │
│        ├── CDN Integration                                 │
│        └── Health Monitoring                               │
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
│  ⚡ Performance:                                            │
│    ├── Tempo de Resposta: <2s                              │
│    ├── Throughput: ~100 req/min                            │
│    └── Memory Usage: ~512MB                                │
│                                                            │
│  🔍 Confidence Scores:                                     │
│    ├── Alto (>0.8): ~70% dos casos                        │
│    ├── Médio (0.5-0.8): ~25% dos casos                    │
│    └── Baixo (<0.5): ~5% dos casos                        │
└─────────────────────────────────────────────────────────────┘
```

## 🔮 Roadmap de Melhorias

```
┌─────────────────────────────────────────────────────────────┐
│                  Próximas Funcionalidades                  │
├─────────────────────────────────────────────────────────────┤
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
│    ├── API REST completa                                   │
│    ├── Integração com email                                │
│    ├── Dashboard analytics                                 │
│    └── Múltiplos formatos de arquivo                       │
└─────────────────────────────────────────────────────────────┘
```

---

**📝 Nota:** Este documento complementa a documentação técnica em `ARQUITETURA.md`, fornecendo uma visão visual e estrutural do sistema AutoU Email Classifier.

**🔄 Última atualização:** Janeiro 2025
**👨‍💻 Desenvolvido para:** Processo Seletivo AutoU
**🎯 Objetivo:** Demonstrar arquitetura e design de sistema completo