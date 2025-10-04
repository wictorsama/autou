# 🚀 Deploy AWS Lambda - AutoU Email Classifier

Esta pasta contém os arquivos de configuração para deploy da aplicação AutoU na AWS Lambda usando Serverless Framework.

## ✅ Status Atual

- **✅ Deploy Realizado**: Janeiro 2025
- **✅ API Funcionando**: `https://x1r6i3udxg.execute-api.us-east-1.amazonaws.com/dev/`
- **✅ Função Lambda**: `autou-email-classifier-dev-app`
- **✅ Região**: us-east-1

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
├── GUIA_AWS_COMPLETO.md  # Documentação completa
└── README.md             # Este arquivo
```

## 🚀 Deploy Rápido

### Pré-requisitos
1. **AWS CLI configurado** com credenciais
2. **Node.js** instalado
3. **Serverless Framework**

### Comandos
```bash
# Navegar para a pasta deploy
cd deploy

# Instalar dependências
npm install

# Deploy
npx serverless deploy

# Verificar status
npx serverless info
```

## 💰 Custos

- **AWS Lambda**: Gratuito até 1M requisições/mês
- **API Gateway**: ~$3.50 por 1M chamadas
- **Total estimado**: $0-5/mês para uso normal
## 📚 Documentação Adicional

- **[GUIA_AWS_COMPLETO.md](./GUIA_AWS_COMPLETO.md)** - Documentação completa com:
  - Configurações detalhadas
  - Troubleshooting
  - Monitoramento
  - Próximos passos

- **[README principal](../README.md)** - Informações gerais do projeto
- **[Documentação técnica](../docs/)** - Arquitetura e especificações

## 🔗 Links Úteis

- [Serverless Framework](https://www.serverless.com/framework/docs/)
- [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
- [API Gateway Documentation](https://docs.aws.amazon.com/apigateway/)

---

**Última atualização**: Janeiro 2025  
**Status**: ✅ Funcionando