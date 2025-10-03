#!/bin/bash

# AutoU - Script de Deploy Automatizado
# Este script facilita o deploy da aplicação em diferentes plataformas

set -e  # Exit on any error

echo "🚀 AutoU - Deploy Script"
echo "========================="

# Função para mostrar ajuda
show_help() {
    echo "Uso: ./deploy.sh [PLATAFORMA] [OPÇÕES]"
    echo ""
    echo "Plataformas disponíveis:"
    echo "  local     - Deploy local com Docker"
    echo "  render    - Deploy no Render.com"
    echo "  railway   - Deploy no Railway"
    echo "  heroku    - Deploy no Heroku"
    echo "  test      - Testa a aplicação localmente"
    echo ""
    echo "Opções:"
    echo "  --build   - Force rebuild da imagem Docker"
    echo "  --help    - Mostra esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  ./deploy.sh local"
    echo "  ./deploy.sh render"
    echo "  ./deploy.sh test"
}

# Função para verificar dependências
check_dependencies() {
    echo "🔍 Verificando dependências..."
    
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 não encontrado. Instale Python 3.11+"
        exit 1
    fi
    
    if ! command -v pip &> /dev/null; then
        echo "❌ pip não encontrado. Instale pip"
        exit 1
    fi
    
    echo "✅ Dependências básicas OK"
}

# Função para deploy local
deploy_local() {
    echo "🐳 Iniciando deploy local com Docker..."
    
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker não encontrado. Instale Docker primeiro."
        exit 1
    fi
    
    # Build da imagem
    if [[ "$1" == "--build" ]] || ! docker images | grep -q "autou"; then
        echo "🔨 Building Docker image..."
        docker build -t autou .
    fi
    
    # Para containers existentes
    echo "🛑 Parando containers existentes..."
    docker-compose down 2>/dev/null || true
    
    # Inicia com docker-compose
    echo "🚀 Iniciando aplicação..."
    docker-compose up -d
    
    echo "✅ Deploy local concluído!"
    echo "📱 Aplicação disponível em: http://localhost:8000"
    echo "📚 Documentação da API: http://localhost:8000/docs"
    echo "🔍 Logs: docker-compose logs -f"
}

# Função para deploy no Render
deploy_render() {
    echo "☁️ Preparando deploy para Render.com..."
    
    if [ ! -f "render.yaml" ]; then
        echo "❌ Arquivo render.yaml não encontrado!"
        exit 1
    fi
    
    echo "✅ Configuração do Render encontrada (render.yaml)"
    echo "📋 Próximos passos:"
    echo "   1. Faça push do código para seu repositório Git"
    echo "   2. Conecte o repositório ao Render.com"
    echo "   3. Configure a variável OPENAI_API_KEY (opcional)"
    echo "   4. O deploy será automático!"
    echo ""
    echo "🔗 Acesse: https://render.com"
}

# Função para deploy no Railway
deploy_railway() {
    echo "🚂 Preparando deploy para Railway..."
    
    if ! command -v railway &> /dev/null; then
        echo "📦 Instalando Railway CLI..."
        npm install -g @railway/cli || {
            echo "❌ Erro ao instalar Railway CLI. Instale Node.js primeiro."
            exit 1
        }
    fi
    
    echo "🔑 Faça login no Railway:"
    railway login
    
    echo "🚀 Iniciando deploy..."
    railway up
    
    echo "✅ Deploy no Railway concluído!"
}

# Função para deploy no Heroku
deploy_heroku() {
    echo "🟣 Preparando deploy para Heroku..."
    
    if ! command -v heroku &> /dev/null; then
        echo "❌ Heroku CLI não encontrado. Instale primeiro:"
        echo "   https://devcenter.heroku.com/articles/heroku-cli"
        exit 1
    fi
    
    echo "🔑 Verificando login no Heroku..."
    heroku auth:whoami || {
        echo "🔑 Faça login no Heroku:"
        heroku login
    }
    
    # Criar app se não existir
    read -p "📝 Nome do app no Heroku (deixe vazio para gerar automaticamente): " app_name
    
    if [ -z "$app_name" ]; then
        heroku create
    else
        heroku create "$app_name" || echo "⚠️ App já existe, continuando..."
    fi
    
    # Configurar variáveis de ambiente
    echo "🔧 Configurando variáveis de ambiente..."
    heroku config:set OPENAI_MODEL=gpt-4o-mini
    heroku config:set ZSL_MODEL=joeddav/xlm-roberta-large-xnli
    heroku config:set MAX_TEXT_CHARS=20000
    
    read -p "🔑 Chave da OpenAI (opcional, pressione Enter para pular): " openai_key
    if [ ! -z "$openai_key" ]; then
        heroku config:set OPENAI_API_KEY="$openai_key"
    fi
    
    echo "🚀 Fazendo deploy..."
    git push heroku main || git push heroku master
    
    echo "✅ Deploy no Heroku concluído!"
    heroku open
}

# Função para testar localmente
test_local() {
    echo "🧪 Testando aplicação localmente..."
    
    check_dependencies
    
    # Instalar dependências se necessário
    if [ ! -d "venv" ]; then
        echo "📦 Criando ambiente virtual..."
        python3 -m venv venv
    fi
    
    echo "📦 Ativando ambiente virtual e instalando dependências..."
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate
    pip install -r requirements.txt
    
    echo "🚀 Iniciando servidor de desenvolvimento..."
    echo "📱 Aplicação estará disponível em: http://localhost:8000"
    echo "⏹️ Pressione Ctrl+C para parar"
    
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
}

# Função principal
main() {
    case "$1" in
        "local")
            deploy_local "$2"
            ;;
        "render")
            deploy_render
            ;;
        "railway")
            deploy_railway
            ;;
        "heroku")
            deploy_heroku
            ;;
        "test")
            test_local
            ;;
        "--help"|"help"|"")
            show_help
            ;;
        *)
            echo "❌ Plataforma '$1' não reconhecida."
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Executar função principal
main "$@"