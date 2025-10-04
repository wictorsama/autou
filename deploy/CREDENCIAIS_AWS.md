# 🔐 Credenciais AWS - AutoU Email Classifier

## ✅ Usuário IAM Criado com Sucesso!

### 📋 Informações de Login
- **URL de Login**: https://997784788206.signin.aws.amazon.com/console
- **Nome do Usuário**: `autou-lambda-deploy`
- **Senha Temporária**: `zLR5(}g{`

⚠️ **IMPORTANTE**: Você precisará alterar a senha no primeiro login!

## 🔑 Próximos Passos para Deploy

### 1. Criar Access Keys para CLI
1. Faça login no Console AWS com as credenciais acima
2. Vá para **IAM** > **Users** > **autou-lambda-deploy**
3. Clique na aba **Security credentials**
4. Clique em **Create access key**
5. Selecione **Command Line Interface (CLI)**
6. Marque "I understand the above recommendation"
7. Clique **Next** > **Create access key**
8. **SALVE** o Access Key ID e Secret Access Key

### 2. Configurar AWS CLI
```bash
# Configure as credenciais
aws configure

# Quando solicitado, insira:
# AWS Access Key ID: [seu-access-key-id]
# AWS Secret Access Key: [seu-secret-access-key]
# Default region name: us-east-1
# Default output format: json
```

### 3. Configurar OpenAI API Key
```bash
# Crie o arquivo .env na pasta deploy
echo "OPENAI_API_KEY=sua-chave-openai-aqui" > deploy\.env
```

### 4. Executar Deploy Automatizado
```bash
# Execute o script completo de deploy
py deploy\deploy_aws_completo.py
```

## 🚀 Deploy em 3 Comandos

Após configurar as credenciais:

```bash
# 1. Configure AWS CLI
aws configure

# 2. Configure OpenAI API Key
echo "OPENAI_API_KEY=sk-sua-chave-aqui" > deploy\.env

# 3. Execute deploy completo
py deploy\deploy_aws_completo.py
```

## 📊 O que o Script Fará

1. ✅ Verificar pré-requisitos
2. ✅ Configurar ambiente Serverless
3. ✅ Executar testes de validação
4. ✅ Criar configuração Lambda
5. ✅ Deploy para AWS (2-5 minutos)
6. ✅ Testar API deployada
7. ✅ Gerar relatório final

## 💰 Custos Estimados

- **Free Tier**: 1M requests/mês por 12 meses
- **Após Free Tier**: ~$1-5/mês para uso moderado
- **Economia vs Render**: $2-20/mês

## 🔒 Segurança

⚠️ **NUNCA** compartilhe suas credenciais AWS!
- Access Key ID e Secret Access Key são sensíveis
- Use apenas em ambiente seguro
- Configure alertas de billing na AWS

## 📞 Suporte

Em caso de problemas:
1. Verifique se as credenciais estão corretas
2. Consulte o <mcfile name="GUIA_COMPLETO_AWS.md" path="deploy/GUIA_COMPLETO_AWS.md"></mcfile>
3. Execute `aws sts get-caller-identity` para testar conexão

---

🎉 **Pronto!** Agora você pode fazer o deploy completo para AWS Lambda!