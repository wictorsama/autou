# 🚀 Guia Completo: AutoU Email Classifier na AWS Lambda

## 📋 Visão Geral

Este guia documenta o processo completo de deploy da aplicação AutoU Email Classifier na AWS Lambda usando Serverless Framework.

## ✅ Status do Deploy

- **✅ Deploy Realizado**: Janeiro 2025
- **✅ API Funcionando**: `https://x1r6i3udxg.execute-api.us-east-1.amazonaws.com/dev/`
- **✅ Função Lambda**: `autou-email-classifier-dev-app`
- **✅ Região**: us-east-1
- **✅ Ambiente**: dev (desenvolvimento)

## 🏗️ Arquitetura Atual

```
API Gateway → AWS Lambda → Handler Básico
```

### Configurações Técnicas
- **Runtime**: Python 3.9
- **Memória**: 512 MB
- **Timeout**: 30 segundos (API Gateway: 29s)
- **Tamanho do pacote**: 87 kB
- **CORS**: Habilitado para todas as origens

## 📁 Estrutura de Arquivos

```
deploy/
├── .env                    # Variáveis de ambiente (não commitado)
├── .env.example           # Exemplo de variáveis de ambiente
├── .serverless/           # Arquivos gerados pelo Serverless
├── handler.py             # Função Lambda principal
├── serverless.yml         # Configuração do Serverless Framework
├── package.json           # Dependências Node.js
├── requirements_aws.txt   # Dependências Python para AWS
└── GUIA_AWS_COMPLETO.md  # Este arquivo
```

## 🔧 Configuração Atual

### handler.py
```python
import json

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        },
        'body': json.dumps({
            'message': 'Hello from AWS Lambda!',
            'status': 'success',
            'service': 'autou-email-classifier'
        })
    }

app = lambda_handler  # Alias para compatibilidade
```

### serverless.yml
```yaml
service: autou-email-classifier

provider:
  name: aws
  runtime: python3.9
  region: us-east-1
  stage: dev
  memorySize: 512
  timeout: 30

functions:
  app:
    handler: handler.lambda_handler
    events:
      - http:
          path: /{proxy+}
          method: ANY
          cors: true
      - http:
          path: /
          method: ANY
          cors: true
```

## 🚀 Como Fazer Deploy

### Pré-requisitos
1. **AWS CLI configurado** com credenciais do usuário `autou-lambda-deploy`
2. **Node.js** instalado
3. **Serverless Framework** instalado globalmente

### Comandos de Deploy
```bash
# Navegar para a pasta deploy
cd deploy

# Instalar dependências Node.js
npm install

# Fazer deploy
npx serverless deploy

# Verificar status
npx serverless info
```

## 🧪 Testes

### Teste Básico da API
```powershell
# PowerShell
Invoke-WebRequest -Uri "https://x1r6i3udxg.execute-api.us-east-1.amazonaws.com/dev/" -Method GET
```

```bash
# Bash/Linux
curl https://x1r6i3udxg.execute-api.us-east-1.amazonaws.com/dev/
```

**Resposta Esperada:**
```json
{
  "message": "Hello from AWS Lambda!",
  "status": "success",
  "service": "autou-email-classifier"
}
```

## 📊 Monitoramento

### CloudWatch Logs
```bash
# Ver logs recentes
aws logs filter-log-events --log-group-name "/aws/lambda/autou-email-classifier-dev-app" --start-time $(date -d '1 hour ago' +%s)000
```

### Métricas Importantes
- **Invocações**: Número de chamadas à função
- **Duração**: Tempo de execução
- **Erros**: Taxa de erro
- **Throttles**: Limitações de concorrência

## 🔄 Próximos Passos

### 1. Integração com FastAPI
- [ ] Configurar serverless-wsgi plugin
- [ ] Integrar aplicação FastAPI existente
- [ ] Configurar dependências Python

### 2. Funcionalidades
- [ ] Implementar classificação de emails
- [ ] Configurar OpenAI API
- [ ] Adicionar processamento de arquivos

### 3. Segurança
- [ ] Configurar autenticação
- [ ] Implementar rate limiting
- [ ] Configurar HTTPS apenas

### 4. Otimização
- [ ] Configurar cache
- [ ] Otimizar cold start
- [ ] Implementar logging estruturado

## 🔐 Credenciais AWS

### Usuário IAM: autou-lambda-deploy
**Permissões configuradas:**
- AWSLambdaFullAccess
- IAMFullAccess
- AmazonAPIGatewayAdministrator
- CloudFormationFullAccess
- AmazonS3FullAccess
- CloudWatchFullAccess

### Configuração AWS CLI
```bash
aws configure
# AWS Access Key ID: [CONFIGURADO]
# AWS Secret Access Key: [CONFIGURADO]
# Default region name: us-east-1
# Default output format: json
```

## 💰 Custos Estimados

### AWS Lambda (Free Tier)
- **1M requisições/mês**: Gratuito
- **400.000 GB-segundos**: Gratuito
- **Após Free Tier**: ~$0.20 por 1M requisições

### API Gateway
- **1M chamadas/mês**: ~$3.50
- **Transferência de dados**: ~$0.09/GB

## 🆘 Troubleshooting

### Problemas Comuns

1. **Handler não encontrado**
   - Verificar `serverless.yml`: `handler: handler.lambda_handler`
   - Verificar se função existe em `handler.py`

2. **Timeout**
   - Aumentar timeout no `serverless.yml`
   - Otimizar código para execução mais rápida

3. **Dependências não encontradas**
   - Verificar `requirements_aws.txt`
   - Usar versões compatíveis com Lambda

4. **CORS Issues**
   - Verificar headers CORS no handler
   - Configurar CORS no `serverless.yml`

### Logs Úteis
```bash
# Deploy com debug
npx serverless deploy --debug

# Ver logs em tempo real
npx serverless logs -f app -t

# Informações do serviço
npx serverless info
```

## 📚 Recursos Adicionais

- [Documentação Serverless Framework](https://www.serverless.com/framework/docs/)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [API Gateway Documentation](https://docs.aws.amazon.com/apigateway/)
- [CloudWatch Logs](https://docs.aws.amazon.com/cloudwatch/)

---

**Última atualização**: Janeiro 2025  
**Status**: ✅ Funcionando  
**Responsável**: Deploy automatizado via Serverless Framework