# 🚀 Guia de Migração para AWS

## 📊 **Comparação: Render vs AWS**

### 🔴 **Limitações do Render (Plano Gratuito)**
- **Memória:** 512MB RAM (insuficiente para modelos ML)
- **CPU:** Compartilhada, baixa performance
- **Timeout:** 15 minutos de inatividade
- **Cold Start:** Demora para "acordar" após inatividade
- **Limitações:** Não suporta modelos pesados como transformers

### 🟢 **Vantagens da AWS**
- **Memória:** Configurável (1GB-8GB+)
- **CPU:** Dedicada, alta performance
- **Escalabilidade:** Auto-scaling baseado em demanda
- **Disponibilidade:** 99.9% uptime
- **Flexibilidade:** Múltiplas opções de deploy

---

## 🎯 **Opções de Deploy na AWS**

### 1. **AWS Lambda + API Gateway** ⚡
**Melhor para:** Uso esporádico, pay-per-use

**Configuração:**
```yaml
# serverless.yml
service: autou-email-classifier

provider:
  name: aws
  runtime: python3.11
  memorySize: 3008  # 3GB RAM
  timeout: 30
  environment:
    OPENAI_API_KEY: ${env:OPENAI_API_KEY}

functions:
  classify:
    handler: app.main.handler
    events:
      - http:
          path: /{proxy+}
          method: ANY
```

**Custos estimados:**
- **Gratuito:** 1M requests/mês
- **Pago:** ~$0.20 por 1M requests

### 2. **AWS ECS Fargate** 🐳
**Melhor para:** Aplicação sempre ativa, tráfego constante

**Configuração:**
```dockerfile
# Dockerfile otimizado para AWS
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Custos estimados:**
- **t3.small:** ~$15/mês (2GB RAM, 2 vCPU)
- **t3.medium:** ~$30/mês (4GB RAM, 2 vCPU)

### 3. **AWS EC2** 💻
**Melhor para:** Controle total, customização máxima

**Instâncias recomendadas:**
- **t3.small:** $15/mês - Para testes
- **t3.medium:** $30/mês - Para produção leve
- **c5.large:** $60/mês - Para alta performance

---

## 🛠️ **Guia de Migração Passo a Passo**

### **Opção 1: AWS Lambda (Recomendado para início)**

#### 1. **Preparar o Código**
```bash
# Instalar Serverless Framework
npm install -g serverless

# Configurar AWS CLI
aws configure
```

#### 2. **Adaptar para Lambda**
```python
# app/lambda_handler.py
from mangum import Mangum
from app.main import app

handler = Mangum(app)
```

#### 3. **Deploy**
```bash
# Deploy para AWS
serverless deploy
```

### **Opção 2: AWS ECS Fargate**

#### 1. **Criar Task Definition**
```json
{
  "family": "autou-email-classifier",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "3072",
  "containerDefinitions": [
    {
      "name": "autou-app",
      "image": "your-ecr-repo/autou:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "OPENAI_API_KEY",
          "value": "your-api-key"
        }
      ]
    }
  ]
}
```

#### 2. **Deploy com Docker**
```bash
# Build e push para ECR
docker build -t autou .
docker tag autou:latest your-account.dkr.ecr.region.amazonaws.com/autou:latest
docker push your-account.dkr.ecr.region.amazonaws.com/autou:latest
```

---

## 🔧 **Otimizações para AWS**

### **1. Reduzir Tamanho do Modelo**
```python
# app/config.py - Configuração otimizada
class Config:
    # Usar modelo mais leve para AWS Lambda
    ZSL_MODEL = "microsoft/DialoGPT-medium" if os.getenv("AWS_LAMBDA_FUNCTION_NAME") else "facebook/bart-large-mnli"
    
    # Cache em S3 para modelos
    MODEL_CACHE_BUCKET = os.getenv("MODEL_CACHE_BUCKET")
```

### **2. Lazy Loading de Modelos**
```python
# app/nlp.py - Carregamento sob demanda
class EmailClassifier:
    def __init__(self):
        self._model = None
        self._tokenizer = None
    
    @property
    def model(self):
        if self._model is None:
            self._load_model()
        return self._model
    
    def _load_model(self):
        # Carregar apenas quando necessário
        pass
```

### **3. Cache com Redis/ElastiCache**
```python
# app/cache.py
import redis

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=6379,
    decode_responses=True
)

def cache_classification(text_hash, result):
    redis_client.setex(f"classification:{text_hash}", 3600, json.dumps(result))
```

---

## 💰 **Análise de Custos**

### **Render (Atual)**
- **Gratuito:** Limitações severas
- **Pago:** $7/mês - Ainda limitado

### **AWS (Estimativas mensais)**
- **Lambda:** $0-5/mês (uso baixo)
- **ECS Fargate:** $15-30/mês
- **EC2 t3.small:** $15/mês
- **EC2 t3.medium:** $30/mês

### **Recomendação de Custo-Benefício:**
1. **Desenvolvimento/Teste:** AWS Lambda
2. **Produção Leve:** ECS Fargate t3.small
3. **Produção Pesada:** EC2 t3.medium

---

## 🚀 **Próximos Passos**

### **Imediato (1-2 dias)**
1. ✅ Criar conta AWS (free tier)
2. ✅ Configurar AWS CLI
3. ✅ Testar deploy com Lambda

### **Curto Prazo (1 semana)**
1. 🔄 Migrar para ECS Fargate
2. 🔄 Configurar domínio personalizado
3. 🔄 Implementar monitoramento

### **Médio Prazo (1 mês)**
1. 📊 Otimizar performance
2. 📊 Implementar auto-scaling
3. 📊 Configurar CI/CD

---

## 📞 **Suporte e Recursos**

- **AWS Free Tier:** 12 meses gratuitos
- **Documentação:** [AWS Lambda](https://docs.aws.amazon.com/lambda/)
- **Tutoriais:** [Serverless Framework](https://www.serverless.com/)
- **Comunidade:** [AWS Community](https://aws.amazon.com/developer/community/)

**A migração para AWS resolverá os problemas de memória e performance que você está enfrentando no Render!** 🎯