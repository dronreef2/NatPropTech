#!/bin/bash

# 🚀 Script de Execução - NatPropTech WhatsApp Business Integration
# Autor: MiniMax Agent
# Data: 17 de Novembro de 2025

echo "================================================================================"
echo "🚀 NATPROPTECH MINIMAX M2 + WHATSAPP BUSINESS"
echo "================================================================================"
echo "🤖 Sistema de IA para Imobiliário com WhatsApp Business integrado"
echo "📱 Acesso via WhatsApp pelo computador com chatbot inteligente"
echo "================================================================================"

# Verificar se estamos no diretório correto
if [ ! -f "app_whatsapp_integrated.py" ]; then
    echo "❌ Erro: Execute este script na pasta /workspace"
    exit 1
fi

# Verificar se Python está disponível
if ! command -v python &> /dev/null; then
    echo "❌ Erro: Python não encontrado"
    exit 1
fi

echo "✅ Ambiente verificado"
echo ""

# Configurar PYTHONPATH
export PYTHONPATH="/workspace:$PYTHONPATH"

# Função para verificar se a porta está ocupada
check_port() {
    if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Porta 8000 já está em uso"
        echo "🔍 Verificando processos..."
        lsof -Pi :8000 -sTCP:LISTEN
        echo ""
        read -p "Deseja parar o processo existente? (s/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Ss]$ ]]; then
            echo "🛑 Parando processo existente..."
            lsof -ti:8000 | xargs kill -9 2>/dev/null
            sleep 2
        else
            echo "❌ Cancelando execução"
            exit 1
        fi
    fi
}

# Função para iniciar o sistema
start_system() {
    echo "🚀 Iniciando NatPropTech WhatsApp Business..."
    echo ""
    echo "🌐 URLs disponíveis após inicialização:"
    echo "   📊 Dashboard: http://localhost:8000/dashboard"
    echo "   🔌 API Health: http://localhost:8000/"
    echo "   💬 WebSocket: ws://localhost:8000/ws"
    echo "   📱 Webhook: https://seu-dominio.com/webhook/whatsapp"
    echo ""
    echo "📋 Funcionalidades ativas:"
    echo "   🤖 Swarm Intelligence (9 agentes)"
    echo "   🧠 MiniMax M2 Agent"
    echo "   💬 WhatsApp Business API"
    echo "   🏠 Chatbot imobiliário"
    echo "   🎯 Qualificação automática de leads"
    echo "   📅 Agendamento de visitas"
    echo "   💰 Simulação de financiamento"
    echo ""
    echo "⏹️  Para parar o sistema: Ctrl+C"
    echo ""
    
    # Executar aplicação
    python app_whatsapp_integrated.py
}

# Função para mostrar ajuda
show_help() {
    echo "📋 Comandos disponíveis:"
    echo "   ./start_whatsapp.sh start   - Iniciar sistema (padrão)"
    echo "   ./start_whatsapp.sh demo    - Executar demonstração"
    echo "   ./start_whatsapp.sh status  - Verificar status"
    echo "   ./start_whatsapp.sh help    - Mostrar esta ajuda"
    echo ""
    echo "📱 Para configurar WhatsApp Business:"
    echo "   1. Edite o arquivo .env com suas credenciais"
    echo "   2. Configure webhook no Meta for Developers"
    echo "   3. Teste com número de telefone real"
    echo ""
    echo "📖 Documentação completa:"
    echo "   WHATSAPP_BUSINESS_GUIDE.md"
    echo "   WHATSAPP_BUSINESS_FINAL_REPORT.md"
}

# Função para executar demonstração
run_demo() {
    echo "🎭 Iniciando demonstração..."
    echo ""
    
    # Verificar se o sistema está rodando
    if curl -s http://localhost:8000/ >/dev/null 2>&1; then
        echo "✅ Sistema detectado rodando na porta 8000"
        echo "🎮 Iniciando demonstração interativa..."
        echo ""
        python demo_whatsapp.py
    else
        echo "❌ Sistema não está rodando na porta 8000"
        echo "💡 Execute primeiro: ./start_whatsapp.sh start"
    fi
}

# Função para verificar status
check_status() {
    echo "🔍 Verificando status do sistema..."
    echo ""
    
    if curl -s http://localhost:8000/ >/dev/null 2>&1; then
        echo "✅ Sistema online na porta 8000"
        echo ""
        echo "📊 Status detalhado:"
        curl -s http://localhost:8000/ | python -m json.tool 2>/dev/null || echo "   Erro ao obter detalhes"
    else
        echo "❌ Sistema offline na porta 8000"
    fi
    
    echo ""
    echo "🔧 Processos Python relacionados:"
    ps aux | grep -E "(app_whatsapp|demo_whatsapp)" | grep -v grep || echo "   Nenhum processo encontrado"
}

# Main script logic
case "${1:-start}" in
    "start")
        check_port
        start_system
        ;;
    "demo")
        run_demo
        ;;
    "status")
        check_status
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        echo "❌ Comando inválido: $1"
        echo ""
        show_help
        exit 1
        ;;
esac