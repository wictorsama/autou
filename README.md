# AutoU - Classificador de E-mails com IA

## 📋 Descrição

O AutoU é um sistema inteligente de classificação e resposta automática de e-mails desenvolvido como MVP (Minimum Viable Product). O sistema utiliza modelos de IA para classificar e-mails como "Produtivos" ou "Improdutivos" e sugere respostas apropriadas.

## 🚀 Funcionalidades

### 🤖 **Inteligência Artificial**
- **Classificação Zero-Shot**: Utiliza o modelo `joeddav/xlm-roberta-large-xnli` para classificar e-mails sem necessidade de treinamento específico
- **Detecção de Intenção**: Identifica 6 tipos de intenção (status, documentos, suporte, agradecimento, social, spam)
- **Sugestão de Respostas**: Gera respostas baseadas em templates ou integração com OpenAI
- **Scores de Confiança**: Exibe níveis de confiança para classificação e intenção (Alta/Média/Baixa)

### 🎨 **Interface Moderna**
- **Dark Mode**: Toggle entre modo claro e escuro com persistência
- **Animações Nativas**: Transições suaves em CSS/JS para melhor UX
- **Gráficos de Confiança**: Barras de progresso visuais com gradientes coloridos
- **Auto-refresh**: Classificação automática após 2 segundos de digitação
- **Feedback Visual**: Estados de loading, notificações e indicadores visuais

### 📱 **PWA (Progressive Web App)**
- **Instalável**: Pode ser instalado como app nativo no dispositivo
- **Service Worker**: Funciona offline e cache inteligente
- **Manifest**: Ícone personalizado e configurações de app
- **Responsivo**: Interface adaptável para desktop e mobile

### 💾 **Persistência Local**
- **Histórico LocalStorage**: Salva classificações localmente no navegador
- **Indicadores Auto-gerados**: Marca entradas criadas via auto-refresh
- **Processamento de Arquivos**: Suporte para arquivos .txt e .pdf
- **API RESTful**: Endpoints para integração com outros sistemas

## 🛠️ Tecnologias

- **Backend**: FastAPI, Python 3.11+, Uvicorn
- **IA/ML**: Transformers (Hugging Face), XLM-RoBERTa, NLTK
- **Frontend**: HTML5, Tailwind CSS, Alpine.js, CSS Animations
- **PWA**: Service Worker, Web App Manifest, LocalStorage
- **Testes**: pytest, TestClient
- **Deploy**: Docker, Render.com, Heroku
- **Arquivos**: PDFMiner, Multipart Forms

## 📦 Instalação

### Pré-requisitos
- Python 3.11 ou superior
- pip

### Configuração Local

1. **Clone o repositório**:
```bash
git clone <repository-url>
cd autou
```

2. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

3. **Configure variáveis de ambiente** (opcional):
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

4. **Execute o servidor**:
```bash
uvicorn app.main:app --reload
```

5. **Acesse a aplicação**:
   - Interface Web: http://localhost:8000
   - Documentação da API: http://localhost:8000/docs

## 📧 Exemplos de Uso

### ✅ **Emails Produtivos** (Requerem Resposta)
```
"Preciso do status do chamado #12345. Quando será resolvido?"
→ Categoria: Produtivo | Intenção: Solicitação de informações

"Segue em anexo o comprovante solicitado para o processo 8821."
→ Categoria: Produtivo | Intenção: Fornecimento de informações
```

### ❌ **Emails Improdutivos** (Não Requerem Resposta)
```
"Feliz Natal a toda a equipe! Obrigado pelo suporte."
→ Categoria: Improdutivo | Intenção: Agradecimento/Felicitação

"OFERTA IMPERDÍVEL! 70% DE DESCONTO! Clique aqui!"
→ Categoria: Improdutivo | Intenção: Spam/Marketing
```

### 🎯 **Testando a Aplicação**
1. Cole um dos exemplos na caixa de texto
2. Clique "Classificar Email" ou aguarde o auto-refresh (2s)
3. Observe os gráficos de confiança e resposta sugerida
4. Teste o dark mode (🌙) e instale como PWA (📱)

## 🧪 Testes

### Executar todos os testes:
```bash
pytest
```

### Executar testes com cobertura:
```bash
pytest --cov=app
```

### Executar testes específicos:
```bash
# Testes da API
pytest tests/test_api.py

# Testes do módulo NLP
pytest tests/test_nlp.py

# Testes dos responders
pytest tests/test_responders.py

# Testes dos utilitários
pytest tests/test_utils.py
```

## 📡 API Endpoints

### `GET /`
Interface web principal

### `GET /health`
Health check do serviço

**Resposta**:
```json
{
  "status": "ok",
  "service": "AutoU Email Classifier"
}
```

### `POST /api/process`
Processa e classifica e-mail

**Parâmetros**:
- `text` (string): Texto do e-mail
- `file` (arquivo): Arquivo .txt ou .pdf (opcional)

**Resposta**:
```json
{
  "category": "Produtivo",
  "intent": "Solicitação de Status",
  "category_score": 0.95,
  "intent_score": 0.87,
  "suggested_reply": "Olá! Recebemos sua solicitação...",
  "reply_source": "template"
}
```

## 🐳 Deploy com Docker

### Build da imagem:
```bash
docker build -t autou .
```

### Executar container:
```bash
docker run -p 8000:8000 autou
```

## ☁️ Deploy no Render.com

1. Conecte seu repositório ao Render.com
2. Use o arquivo `render.yaml` para configuração automática
3. Configure as variáveis de ambiente necessárias

## 🔧 Configuração

### Variáveis de Ambiente

- `OPENAI_API_KEY`: Chave da API OpenAI (opcional)
- `OPENAI_MODEL`: Modelo OpenAI a usar (padrão: gpt-3.5-turbo)
- `ZSL_MODEL`: Modelo de classificação zero-shot
- `HOST`: Host do servidor (padrão: 0.0.0.0)
- `PORT`: Porta do servidor (padrão: 8000)
- `MAX_TEXT_LENGTH`: Limite de caracteres para texto

## 📁 Estrutura do Projeto

```
autou/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app e endpoints
│   ├── nlp.py               # Classificação zero-shot com XLM-RoBERTa
│   ├── responders.py        # Templates de resposta inteligentes
│   ├── utils.py             # Utilitários para arquivos PDF/TXT
│   ├── models/
│   │   └── __init__.py
│   ├── static/
│   │   ├── app.js           # JavaScript com Alpine.js e PWA
│   │   ├── styles.css       # CSS com dark mode e animações
│   │   ├── icon.svg         # Ícone do PWA
│   │   ├── manifest.json    # Manifest do PWA
│   │   └── sw.js            # Service Worker
│   └── templates/
│       └── index.html       # Interface web moderna
├── sample_emails/           # E-mails de exemplo para teste
│   ├── produtivo_anexo.txt
│   ├── produtivo_status.txt
│   ├── improdutivo_felicitacao.txt
│   └── improdutivo_spam.txt
├── tests/                   # Testes automatizados completos
│   ├── test_api.py
│   ├── test_nlp.py
│   ├── test_responders.py
│   └── test_utils.py
├── requirements.txt         # Dependências Python atualizadas
├── ARQUITETURA.md          # Documentação técnica detalhada
├── DESIGN_ARCHITECTURE.md  # Arquitetura de design e UX
├── Dockerfile              # Configuração Docker
├── Procfile                # Configuração Heroku
├── render.yaml             # Configuração Render.com
├── pytest.ini              # Configuração pytest
└── README.md               # Este arquivo
```

## 🔒 Privacidade e LGPD

- Processamento local dos dados
- Não armazenamento de e-mails
- Integração opcional com OpenAI (configurável)
- Logs mínimos para debugging

## 🚧 Roadmap

- [ ] Extração de IDs de tickets
- [ ] Dashboard de métricas
- [ ] Fila assíncrona para processamento
- [ ] Integração com SSO
- [ ] Suporte a mais formatos de arquivo
- [ ] Interface de administração

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para suporte, abra uma issue no repositório ou entre em contato através do e-mail de suporte.