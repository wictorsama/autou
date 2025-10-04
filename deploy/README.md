# 🚀 Deploy e Configuração

Esta pasta contém arquivos e scripts relacionados ao deploy e configuração da aplicação AutoU.

## 🆕 **NOVO: Migração para AWS Lambda**

Devido às limitações de memória do Render para modelos de ML, agora oferecemos migração completa para AWS Lambda:

### 📁 Arquivos AWS
- `GUIA_MIGRACAO_AWS.md` - Guia completo de migração
- `setup_aws_lambda.py` - Script de configuração automática
- `lambda_config.py` - Configurações otimizadas para Lambda
- `test_before_deploy.py` - Testes antes do deploy

### 🚀 Migração Rápida (5 minutos)
```bash
# 1. Configurar AWS CLI
aws configure

# 2. Instalar Serverless Framework
npm install -g serverless

# 3. Executar configuração automática
python deploy/setup_aws_lambda.py

# 4. Configurar variáveis
cp .env.example .env
# Editar .env com OPENAI_API_KEY

# 5. Testar
python deploy/test_before_deploy.py

# 6. Deploy
serverless deploy
```

**💰 Custo**: ~$2-20/mês (vs $25-85 no Render)  
**⚡ Performance**: 3GB RAM dedicada  
**🔧 Escalabilidade**: Automática  

---

## 📁 Arquivos Render (Legado)

### 🔧 **deploy.sh**
Script automatizado para deploy em diferentes plataformas.

**Uso:**
```bash
# Deploy local com Docker
./deploy/deploy.sh local

# Deploy no Render.com
./deploy/deploy.sh render

# Deploy no Railway
./deploy/deploy.sh railway

# Deploy no Heroku
./deploy/deploy.sh heroku

# Teste local
./deploy/deploy.sh test
```

**Opções:**
- `--build`: Force rebuild da imagem Docker
- `--help`: Mostra ajuda completa

### ⚙️ **.env.example**
Template de variáveis de ambiente para configuração local.

**Configuração:**
```bash
# Copie o arquivo para a raiz do projeto
cp deploy/.env.example .env

# Edite as variáveis conforme necessário
nano .env
```

**Variáveis disponíveis:**
- `OPENAI_API_KEY`: Chave da API OpenAI (opcional)
- `OPENAI_MODEL`: Modelo OpenAI (padrão: gpt-4o-mini)
- `ZSL_MODEL`: Modelo de classificação zero-shot
- `HOST`: Host do servidor (padrão: 0.0.0.0)
- `PORT`: Porta do servidor (padrão: 8000)
- `MAX_TEXT_CHARS`: Limite de caracteres por texto

## 🐳 Arquivos de Deploy na Raiz

Os seguintes arquivos permanecem na raiz do projeto por serem automaticamente detectados pelas plataformas:

- `Dockerfile` - Configuração do container Docker
- `docker-compose.yml` - Orquestração de containers
- `render.yaml` - Configuração do Render.com
- `Procfile` - Configuração do Heroku
- `requirements.txt` - Dependências Python
- `.dockerignore` - Exclusões do Docker
- `pytest.ini` - Configuração de testes

## 📚 Documentação

Para instruções detalhadas de deploy, consulte:
- [README principal](../README.md) - Seção "🚀 Deploy em Produção"
- [Documentação técnica](../docs/) - Arquitetura e configurações avançadas

## 🔍 Verificação

Após o deploy, teste os endpoints:
```bash
# Health check
curl https://your-app-url.com/health

# Teste de classificação
curl -X POST https://your-app-url.com/api/process \
  -F "text=Preciso de ajuda com o sistema"
```