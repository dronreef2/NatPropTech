#!/bin/bash

# 🚀 NatPropTech MiniMax M2 - Script de Inicialização Completa
# Autor: MiniMax Agent
# Data: 17 de Novembro de 2025

set -e  # Exit on any error

echo "🏡 NatPropTech MiniMax M2 - Sistema de Swarm Intelligence"
echo "============================================================="
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para print colorizado
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Verificar se Python está instalado
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d" " -f2 | cut -d"." -f1-2)
        print_status "Python $PYTHON_VERSION encontrado"
    else
        print_error "Python 3.8+ não encontrado. Por favor, instale Python 3.8 ou superior."
        exit 1
    fi
}

# Verificar se pip está disponível
check_pip() {
    if command -v pip3 &> /dev/null; then
        print_status "pip3 encontrado"
    else
        print_error "pip3 não encontrado. Instale pip3 primeiro."
        exit 1
    fi
}

# Verificar se virtualenv está disponível
check_virtualenv() {
    if command -v python3 -m venv &> /dev/null; then
        print_status "virtualenv disponível"
    else
        print_warning "virtualenv não encontrado. Tentando instalar..."
        pip3 install --user virtualenv
        print_status "virtualenv instalado"
    fi
}

# Criar ambiente virtual
create_virtualenv() {
    if [ -d "natproptech_env" ]; then
        print_info "Ambiente virtual já existe. Reutilizando..."
        source natproptech_env/bin/activate
    else
        print_info "Criando ambiente virtual..."
        python3 -m venv natproptech_env
        source natproptech_env/bin/activate
        print_status "Ambiente virtual criado e ativado"
    fi
}

# Instalar dependências
install_dependencies() {
    print_info "Instalando dependências..."
    
    # Upgrade pip primeiro
    pip install --upgrade pip
    
    # Instalar dependências principais
    pip install fastapi uvicorn[standard] python-multipart
    pip install google-generativeai google-ai-generativelanguage google-ai-generative-ai
    pip install google-auth google-auth-oauthlib google-auth-httplib2
    pip install numpy pandas networkx aiohttp httpx requests
    pip install PyJWT python-dotenv pydantic
    pip install google-cloud-bigquery
    
    print_status "Dependências principais instaladas"
    
    # Instalar dependências avançadas (opcionais)
    print_info "Instalando dependências avançadas..."
    pip install structlog rich pytest pytest-asyncio
    pip install matplotlib plotly streamlit
    pip install python-jose[cryptography] passlib[bcrypt]
    pip install slowapi tenacity
    
    print_status "Dependências avançadas instaladas"
}

# Verificar APIs Keys
check_api_keys() {
    print_info "Verificando configuração de APIs..."
    
    if [ -f ".env" ]; then
        source .env
        print_status "Arquivo .env encontrado"
    else
        print_warning "Arquivo .env não encontrado"
        
        # Tentar carregar de variáveis de ambiente
        if [ -n "$GEMINI_API_KEY" ] && [ -n "$MINIMAX_TOKEN" ]; then
            print_status "APIs Keys encontradas nas variáveis de ambiente"
        else
            print_warning "APIs Keys não configuradas"
            echo ""
            echo "Por favor, configure suas APIs keys:"
            echo "1. GEMINI_API_KEY para Google Gemini"
            echo "2. MINIMAX_TOKEN para MiniMax M2"
            echo ""
            echo "Opções:"
            echo "a) Criar arquivo .env agora"
            echo "b) Definir variáveis de ambiente"
            echo "c) Continuar sem APIs (modo demo)"
            echo ""
            read -p "Escolha (a/b/c): " choice
            
            case $choice in
                a|A)
                    create_env_file
                    ;;
                b|B)
                    set_env_vars
                    ;;
                c|C)
                    print_warning "Continuando em modo demo - funcionalidades limitadas"
                    ;;
                *)
                    print_error "Opção inválida"
                    exit 1
                    ;;
            esac
        fi
    fi
}

# Criar arquivo .env
create_env_file() {
    print_info "Criando arquivo .env..."
    
    echo "# NatPropTech MiniMax M2 - Configuration" > .env
    echo "# Generated on $(date)" >> .env
    echo "" >> .env
    
    echo "GEMINI_API_KEY=" >> .env
    echo "MINIMAX_TOKEN=" >> .env
    
    print_warning "Por favor, edite o arquivo .env e adicione suas APIs keys:"
    echo "  nano .env"
    echo "  # Adicione suas keys nas linhas apropriadas"
    echo ""
}

# Definir variáveis de ambiente
set_env_vars() {
    print_info "Defina suas APIs keys:"
    
    echo -n "Digite sua GEMINI_API_KEY: "
    read -s gemini_key
    echo ""
    
    echo -n "Digite sua MINIMAX_TOKEN: "
    read -s minimax_token
    echo ""
    
    if [ -n "$gemini_key" ] && [ -n "$minimax_token" ]; then
        export GEMINI_API_KEY="$gemini_key"
        export MINIMAX_TOKEN="$minimax_token"
        print_status "APIs Keys configuradas para esta sessão"
        print_info "Para tornar permanente, adicione ao seu ~/.bashrc ou ~/.zshrc"
    else
        print_warning "Keys inválidas. Continuando em modo demo."
    fi
}

# Verificar Google Cloud
check_gcp() {
    print_info "Verificando Google Cloud..."
    
    if command -v gcloud &> /dev/null; then
        print_status "Google Cloud CLI encontrado"
        
        if gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "."; then
            print_status "Autenticado no Google Cloud"
        else
            print_warning "Não autenticado no Google Cloud"
            echo "Execute: gcloud auth login"
        fi
    else
        print_warning "Google Cloud CLI não encontrado"
        print_info "Para funcionalidades completas, instale em: https://cloud.google.com/sdk/docs/install"
    fi
}

# Criar diretórios necessários
create_directories() {
    print_info "Criando estrutura de diretórios..."
    
    mkdir -p logs
    mkdir -p data
    mkdir -p temp
    mkdir -p backups
    
    print_status "Diretórios criados"
}

# Executar testes
run_tests() {
    print_info "Executando testes básicos..."
    
    # Teste de importação
    python3 -c "
import sys
sys.path.append('.')
try:
    import fastapi, uvicorn, numpy, pandas, aiohttp
    print('✅ Dependências principais OK')
except ImportError as e:
    print(f'❌ Erro de importação: {e}')
    sys.exit(1)
"
    
    if [ $? -eq 0 ]; then
        print_status "Testes básicos passaram"
    else
        print_error "Testes falharam. Verifique as dependências."
        exit 1
    fi
}

# Iniciar sistema
start_system() {
    print_info "Iniciando NatPropTech MiniMax M2..."
    
    # Verificar se deve usar demo mode
    DEMO_MODE=false
    
    if [ -z "$GEMINI_API_KEY" ] && [ -z "$MINIMAX_TOKEN" ] && [ ! -f ".env" ]; then
        print_warning "Modo Demo ativado - funcionalidades limitadas"
        DEMO_MODE=true
    fi
    
    echo ""
    echo "🚀 Iniciando servidor..."
    echo "📊 Dashboard: http://localhost:8000/dashboard"
    echo "📡 API: http://localhost:8000"
    echo "📖 Docs: http://localhost:8000/docs"
    echo ""
    echo "Pressione Ctrl+C para parar o servidor"
    echo ""
    
    # Iniciar com uvicorn
    if [ "$DEMO_MODE" = true ]; then
        print_info "Iniciando em modo demo..."
        uvloop=""  # Desabilitar uvloop em modo demo para melhor debug
    else
        uvloop="--loop uvloop"
    fi
    
    # Usar uma das opções disponíveis
    if command -v uvicorn &> /dev/null; then
        python3 -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload $uvloop
    else
        print_error "uvicorn não encontrado. Execute: pip install uvicorn"
        exit 1
    fi
}

# Função de demonstração rápida
run_demo() {
    print_info "Executando demonstração rápida..."
    
    python3 -c "
import asyncio
import sys
sys.path.append('.')

# Importar swarm system (modo demo)
try:
    from swarm_intelligence_system import MiniMaxSwarmIntelligence, TaskComplexity
    
    async def demo():
        print('🚀 Iniciando demonstração do Swarm Intelligence...')
        
        swarm = MiniMaxSwarmIntelligence()
        agents = await swarm.bootstrap_swarm()
        
        print(f'✅ {len(agents)} agentes inicializados')
        
        # Teste básico de tarefa
        task_id = await swarm.submit_swarm_task('lead_qualification', {
            'name': 'João Silva',
            'email': 'joao@email.com',
            'message': 'Interessado em apartamento 3 quartos em Natal'
        }, TaskComplexity.SIMPLE)
        
        print(f'📋 Tarefa submetida: {task_id}')
        print('⏳ Aguardando processamento...')
        
        await asyncio.sleep(5)
        
        status = await swarm.get_swarm_status()
        print(f'📊 Status: {status[\"swarm_size\"]} agentes ativos')
        print(f'📈 Taxa de sucesso: {status[\"tasks\"][\"success_rate\"]:.1%}')
        
        print('✅ Demonstração concluída!')
        print('🌐 Para interface completa, execute: python app.py')
    
    asyncio.run(demo())
    
except ImportError as e:
    print(f'❌ Erro na demonstração: {e}')
    print('ℹ️ Execute a instalação completa primeiro')
except Exception as e:
    print(f'❌ Erro inesperado: {e}')
"
}

# Menu principal
show_menu() {
    echo ""
    echo "🏡 NatPropTech MiniMax M2 - Menu de Opções"
    echo "=========================================="
    echo "1) Instalação Completa"
    echo "2) Modo Rápido (demo apenas)"
    echo "3) Verificar Sistema"
    echo "4) Executar Demonstração"
    echo "5) Iniciar Interface Web"
    echo "6) Limpar Cache"
    echo "7) Sair"
    echo ""
    read -p "Escolha uma opção (1-7): " choice
}

# Verificar sistema
check_system() {
    print_info "Verificando sistema..."
    
    echo "🔧 Python: $(python3 --version 2>&1)"
    echo "📦 pip: $(pip3 --version 2>&1)"
    echo "🌐 FastAPI: $(python3 -c 'import fastapi; print(fastapi.__version__)' 2>&1 || echo 'Não instalado')"
    echo "🧠 NumPy: $(python3 -c 'import numpy; print(numpy.__version__)' 2>&1 || echo 'Não instalado')"
    echo "🔗 aiohttp: $(python3 -c 'import aiohttp; print(aiohttp.__version__)' 2>&1 || echo 'Não instalado')"
    
    # Verificar APIs
    if [ -n "$GEMINI_API_KEY" ]; then
        echo "🤖 Gemini API: ✅ Configurado"
    else
        echo "🤖 Gemini API: ❌ Não configurado"
    fi
    
    if [ -n "$MINIMAX_TOKEN" ]; then
        echo "🚀 MiniMax API: ✅ Configurado"  
    else
        echo "🚀 MiniMax API: ❌ Não configurado"
    fi
    
    print_status "Verificação concluída"
}

# Limpar cache
clean_cache() {
    print_info "Limpando cache..."
    
    rm -rf __pycache__
    rm -rf *.pyc
    rm -rf .pytest_cache
    rm -rf .coverage
    rm -rf logs/*.log
    rm -rf temp/*
    
    print_status "Cache limpo"
}

# Função principal
main() {
    echo ""
    show_menu
    
    case $choice in
        1)
            print_info "Iniciando instalação completa..."
            check_python
            check_pip
            check_virtualenv
            create_virtualenv
            install_dependencies
            check_api_keys
            check_gcp
            create_directories
            run_tests
            start_system
            ;;
        2)
            print_info "Modo rápido - demonstração apenas..."
            check_python
            run_demo
            ;;
        3)
            check_system
            ;;
        4)
            run_demo
            ;;
        5)
            start_system
            ;;
        6)
            clean_cache
            ;;
        7)
            print_status "Saindo..."
            exit 0
            ;;
        *)
            print_error "Opção inválida"
            main
            ;;
    esac
}

# Verificar se é execução direta
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi