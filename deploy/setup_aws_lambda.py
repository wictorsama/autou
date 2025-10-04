#!/usr/bin/env python3
"""
Script de configuração automática para deploy na AWS Lambda
Autor: AutoU Email Classifier
Data: 03 de Outubro de 2025
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def check_requirements():
    """Verifica se os requisitos estão instalados"""
    print("🔍 Verificando requisitos...")
    
    # Verificar AWS CLI
    try:
        result = subprocess.run(['aws', '--version'], capture_output=True, text=True)
        print(f"✅ AWS CLI: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ AWS CLI não encontrado. Instale: https://aws.amazon.com/cli/")
        return False
    
    # Verificar Serverless Framework
    try:
        result = subprocess.run(['serverless', '--version'], capture_output=True, text=True)
        print(f"✅ Serverless: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Serverless Framework não encontrado.")
        print("   Instale com: npm install -g serverless")
        return False
    
    return True

def create_serverless_config():
    """Cria configuração do Serverless Framework"""
    print("📝 Criando configuração serverless.yml...")
    
    config = {
        'service': 'autou-email-classifier',
        'frameworkVersion': '3',
        'provider': {
            'name': 'aws',
            'runtime': 'python3.11',
            'region': 'us-east-1',
            'memorySize': 3008,  # 3GB
            'timeout': 30,
            'environment': {
                'OPENAI_API_KEY': '${env:OPENAI_API_KEY}',
                'OPENAI_MODEL': 'gpt-4o-mini',
                'ZSL_MODEL': 'microsoft/DialoGPT-medium',  # Modelo mais leve
                'MAX_TEXT_CHARS': '10000',
                'ENABLE_MEMORY_CLEANUP': 'true'
            }
        },
        'functions': {
            'api': {
                'handler': 'lambda_handler.handler',
                'events': [
                    {
                        'http': {
                            'path': '/{proxy+}',
                            'method': 'ANY',
                            'cors': True
                        }
                    },
                    {
                        'http': {
                            'path': '/',
                            'method': 'ANY',
                            'cors': True
                        }
                    }
                ]
            }
        },
        'plugins': [
            'serverless-python-requirements'
        ],
        'custom': {
            'pythonRequirements': {
                'dockerizePip': True,
                'zip': True,
                'slim': True,
                'strip': False,
                'noDeps': [
                    'boto3',
                    'botocore'
                ]
            }
        }
    }
    
    with open('serverless.yml', 'w') as f:
        import yaml
        yaml.dump(config, f, default_flow_style=False)
    
    print("✅ serverless.yml criado")

def create_lambda_handler():
    """Cria o handler para AWS Lambda"""
    print("📝 Criando lambda_handler.py...")
    
    handler_code = '''import os
import sys

# Adicionar o diretório app ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

try:
    from mangum import Mangum
    from app.main import app
    
    # Configurar para ambiente Lambda
    os.environ.setdefault('AWS_LAMBDA_FUNCTION_NAME', 'true')
    
    # Criar handler do Mangum
    handler = Mangum(app, lifespan="off")
    
except ImportError as e:
    print(f"Erro de importação: {e}")
    
    def handler(event, context):
        return {
            'statusCode': 500,
            'body': f'Erro de importação: {str(e)}'
        }
'''
    
    with open('lambda_handler.py', 'w') as f:
        f.write(handler_code)
    
    print("✅ lambda_handler.py criado")

def update_requirements():
    """Atualiza requirements.txt para Lambda"""
    print("📝 Atualizando requirements.txt para Lambda...")
    
    # Ler requirements atual
    with open('requirements.txt', 'r') as f:
        requirements = f.read()
    
    # Adicionar dependências específicas do Lambda
    lambda_deps = '''
# AWS Lambda específico
mangum>=0.17.0,<0.18.0
'''
    
    # Escrever requirements atualizado
    with open('requirements.txt', 'w') as f:
        f.write(requirements + lambda_deps)
    
    print("✅ requirements.txt atualizado")

def create_package_json():
    """Cria package.json para plugins do Serverless"""
    print("📝 Criando package.json...")
    
    package = {
        "name": "autou-email-classifier",
        "version": "1.0.0",
        "description": "AutoU Email Classifier - AWS Lambda",
        "devDependencies": {
            "serverless-python-requirements": "^6.0.0"
        }
    }
    
    with open('package.json', 'w') as f:
        json.dump(package, f, indent=2)
    
    print("✅ package.json criado")

def install_dependencies():
    """Instala dependências do Node.js"""
    print("📦 Instalando dependências...")
    
    try:
        subprocess.run(['npm', 'install'], check=True)
        print("✅ Dependências instaladas")
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências")
        return False
    
    return True

def create_env_example():
    """Cria arquivo .env.example"""
    print("📝 Criando .env.example...")
    
    env_content = '''# Configurações para AWS Lambda
OPENAI_API_KEY=sua_chave_openai_aqui
AWS_REGION=us-east-1
AWS_PROFILE=default

# Opcional: Para desenvolvimento local
DEBUG=false
LOG_LEVEL=INFO
'''
    
    with open('.env.example', 'w') as f:
        f.write(env_content)
    
    print("✅ .env.example criado")

def create_deploy_script():
    """Cria script de deploy"""
    print("📝 Criando script de deploy...")
    
    deploy_script = '''#!/bin/bash

# Script de deploy para AWS Lambda
echo "🚀 Iniciando deploy para AWS Lambda..."

# Verificar se .env existe
if [ ! -f ".env" ]; then
    echo "❌ Arquivo .env não encontrado!"
    echo "   Copie .env.example para .env e configure suas variáveis"
    exit 1
fi

# Carregar variáveis de ambiente
export $(cat .env | xargs)

# Verificar OPENAI_API_KEY
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY não configurada!"
    exit 1
fi

# Deploy
echo "📦 Fazendo deploy..."
serverless deploy

if [ $? -eq 0 ]; then
    echo "✅ Deploy realizado com sucesso!"
    echo "🌐 Sua API está disponível nos endpoints mostrados acima"
else
    echo "❌ Erro no deploy"
    exit 1
fi
'''
    
    with open('deploy_lambda.sh', 'w') as f:
        f.write(deploy_script)
    
    # Tornar executável no Unix
    if os.name != 'nt':
        os.chmod('deploy_lambda.sh', 0o755)
    
    print("✅ deploy_lambda.sh criado")

def main():
    """Função principal"""
    print("🚀 AutoU Email Classifier - Setup AWS Lambda")
    print("=" * 50)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('app/main.py'):
        print("❌ Execute este script no diretório raiz do projeto")
        sys.exit(1)
    
    # Verificar requisitos
    if not check_requirements():
        print("\n❌ Instale os requisitos antes de continuar")
        sys.exit(1)
    
    print("\n📋 Configurando projeto para AWS Lambda...")
    
    try:
        create_serverless_config()
        create_lambda_handler()
        update_requirements()
        create_package_json()
        create_env_example()
        create_deploy_script()
        
        if install_dependencies():
            print("\n🎉 Configuração concluída com sucesso!")
            print("\n📋 Próximos passos:")
            print("1. Copie .env.example para .env")
            print("2. Configure sua OPENAI_API_KEY no .env")
            print("3. Configure AWS CLI: aws configure")
            print("4. Execute: ./deploy_lambda.sh (Linux/Mac) ou serverless deploy")
            print("\n💡 Documentação completa em: deploy/GUIA_MIGRACAO_AWS.md")
        
    except Exception as e:
        print(f"\n❌ Erro durante configuração: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()