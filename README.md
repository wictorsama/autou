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

3.2. **Configure variáveis de ambiente** (opcional):
```bash
cp deploy/.env.example .env
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

## 🚀 Deploy em Produção

### 🐳 Deploy com Docker

#### Build da imagem:
```bash
docker build -t autou .
```

#### Executar container:
```bash
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key_here autou
```

#### Docker Compose (recomendado):
```yaml
version: '3.8'
services:
  autou:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENAI_MODEL=gpt-4o-mini
      - ZSL_MODEL=joeddav/xlm-roberta-large-xnli
      - MAX_TEXT_CHARS=20000
```

### ☁️ Deploy no Render.com (Recomendado)

#### Configuração Automática:
1. **Fork/Clone** este repositório
2. **Conecte** seu repositório ao [Render.com](https://render.com)
3. **Importe** o projeto - o arquivo `render.yaml` será detectado automaticamente
4. **Configure** as variáveis de ambiente:
   - `OPENAI_API_KEY`: Sua chave da OpenAI (opcional, mas recomendado)
   - Outras variáveis já estão pré-configuradas no `render.yaml`
5. **Deploy** será iniciado automaticamente

#### Script Automatizado:
```bash
# Use o script de deploy para Render
./deploy/deploy.sh render
```

#### Configuração Manual:
1. Crie um novo **Web Service** no Render
2. Conecte seu repositório GitHub
3. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3
4. Adicione as variáveis de ambiente necessárias

### 🚂 Deploy no Railway

#### Script Automatizado:
```bash
# Use o script de deploy para Railway
./deploy/deploy.sh railway
```

#### Configuração Manual:
1. Conecte seu repositório ao [Railway](https://railway.app)
2. Configure as variáveis de ambiente:
   ```
   OPENAI_API_KEY=your_key_here
   OPENAI_MODEL=gpt-4o-mini
   ZSL_MODEL=joeddav/xlm-roberta-large-xnli
   MAX_TEXT_CHARS=20000
   ```
3. O deploy será automático usando o `Dockerfile`

### 🟣 Deploy no Heroku

#### Script Automatizado:
```bash
# Use o script de deploy para Heroku
./deploy/deploy.sh heroku
```

#### Configuração Manual:
1. Instale o [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Execute os comandos:
   ```bash
   heroku create your-app-name
   heroku config:set OPENAI_API_KEY=your_key_here
   heroku config:set OPENAI_MODEL=gpt-4o-mini
   git push heroku main
   ```

### ☁️ Deploy na AWS (EC2 + Docker)

1. **Lance uma instância EC2** (t2.micro para teste)
2. **Instale Docker**:
   ```bash
   sudo yum update -y
   sudo yum install -y docker
   sudo service docker start
   ```
3. **Clone e execute**:
   ```bash
   git clone your-repo-url
   cd autou
   sudo docker build -t autou .
   sudo docker run -d -p 80:8000 -e OPENAI_API_KEY=your_key autou
   ```

### 🔧 Variáveis de Ambiente para Produção

| Variável | Obrigatória | Padrão | Descrição |
|----------|-------------|--------|-----------|
| `OPENAI_API_KEY` | Não | - | Chave da API OpenAI para respostas inteligentes |
| `OPENAI_MODEL` | Não | `gpt-4o-mini` | Modelo OpenAI a utilizar |
| `ZSL_MODEL` | Não | `joeddav/xlm-roberta-large-xnli` | Modelo de classificação |
| `HOST` | Não | `0.0.0.0` | Host do servidor |
| `PORT` | Não | `8000` | Porta do servidor |
| `MAX_TEXT_CHARS` | Não | `20000` | Limite de caracteres por texto |

### 🔍 Verificação do Deploy

Após o deploy, teste os endpoints:

```bash
# Health check
curl https://your-app-url.com/health

# Teste de classificação
curl -X POST https://your-app-url.com/api/process \
  -F "text=Preciso de ajuda com o sistema"
```

### 📊 Monitoramento

- **Logs**: Acesse via dashboard da plataforma escolhida
- **Métricas**: CPU, memória e tempo de resposta
- **Health Check**: Endpoint `/health` para monitoramento automático

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
├── app/                     # Aplicação principal
│   ├── main.py              # FastAPI app e endpoints
│   ├── nlp.py               # Classificação zero-shot com XLM-RoBERTa
│   ├── responders.py        # Templates de resposta inteligentes
│   ├── utils.py             # Utilitários para arquivos PDF/TXT
│   ├── static/              # Arquivos estáticos (CSS, JS, PWA)
│   └── templates/           # Interface web moderna
├── deploy/                  # 🚀 Scripts e configurações de deploy
│   ├── README.md            # Instruções de deploy e configuração
│   ├── deploy.sh            # Script automatizado de deploy
│   └── .env.example         # Template de variáveis de ambiente
├── docs/                    # 📚 Documentação técnica detalhada
│   ├── README.md            # Índice da documentação
│   ├── ARQUITETURA.md       # Documentação técnica completa
│   ├── DESIGN_ARCHITECTURE.md # Arquitetura de design e UX
│   └── MVP_INICIAL.md       # Documentação histórica do MVP
├── sample_emails/           # E-mails de exemplo para teste
├── tests/                   # Testes automatizados completos
├── tests_temp/              # Arquivos de teste temporários
├── requirements.txt         # Dependências Python
├── Dockerfile              # Configuração Docker
├── render.yaml             # Configuração Render.com
└── README.md               # Este arquivo
```

## 📚 Documentação Técnica

Para informações técnicas detalhadas, consulte a [documentação completa](./docs/):

- **[Arquitetura do Sistema](./docs/ARQUITETURA.md)** - Documentação técnica completa
- **[Design e UX](./docs/DESIGN_ARCHITECTURE.md)** - Arquitetura visual e fluxos
- **[Índice da Documentação](./docs/README.md)** - Guia completo da documentação

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