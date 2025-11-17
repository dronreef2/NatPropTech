#!/bin/bash

# NatPropTech - Sistema de Implementação de Ferramentas Agênticas
# Script de deploy e configuração completa
# 
# Autor: MiniMax Agent
# Data: 17 de Novembro de 2025

set -e

echo "🏡 NatPropTech - Deploy de Ferramentas Agênticas"
echo "================================================"

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configurações
PROJECT_NAME="natproptech-agentic"
PYTHON_VERSION="3.9"
VENV_NAME="natproptech_env"

print_step() {
    echo -e "${BLUE}[PASSO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[AVISO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERRO]${NC} $1"
}

# Função para verificar se comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Função para instalar dependências Python
install_python_dependencies() {
    print_step "Instalando dependências Python..."
    
    # Lista de dependências necessárias
    cat > requirements.txt << EOF
# Core AI/ML
openai>=1.0.0
google-generativeai>=0.3.0
google-ai-generativelanguage>=0.6.0

# Web APIs e HTTP
aiohttp>=3.8.0
requests>=2.28.0
httpx>=0.24.0

# Data Processing
pandas>=1.5.0
numpy>=1.24.0
python-dateutil>=2.8.0

# Configuration and Environment
python-dotenv>=1.0.0
pyyaml>=6.0
configparser>=5.3.0

# Logging and Monitoring
loguru>=0.7.0
prometheus-client>=0.16.0

# Database (Opcional)
sqlite3
sqlalchemy>=2.0.0
alembic>=1.11.0

# Testing
pytest>=7.0.0
pytest-asyncio>=0.21.0
pytest-mock>=3.10.0

# Development
black>=23.0.0
flake8>=6.0.0
mypy>=1.4.0

# Performance
uvloop>=0.17.0
redis>=4.5.0

# Other utilities
asyncio-mqtt>=0.11.0
jsonschema>=4.17.0
pydantic>=2.0.0
EOF
    
    # Instala dependências
    pip install -r requirements.txt
    
    print_success "Dependências Python instaladas"
}

# Função para configurar variáveis de ambiente
setup_environment() {
    print_step "Configurando variáveis de ambiente..."
    
    cat > .env.example << EOF
# MiniMax Agent Configuration
MINIMAX_API_KEY=your_minimax_api_key_here
MINIMAX_MODEL=gemini-pro
MINIMAX_MAX_TOKENS=2048

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2048

# WhatsApp Business API
WHATSAPP_ACCESS_TOKEN=your_whatsapp_access_token_here
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id_here
WHATSAPP_VERIFY_TOKEN=natproptech_verify_token
WHATSAPP_BUSINESS_ACCOUNT_ID=your_business_account_id_here

# Respond.io Integration (Recomendado para NatPropTech)
RESPONDIO_API_KEY=your_respondio_api_key_here
RESPONDIO_WORKSPACE_ID=your_workspace_id_here
RESPONDIO_WEBHOOK_SECRET=your_webhook_secret_here

# Database Configuration
DATABASE_URL=sqlite:///natproptech.db
REDIS_URL=redis://localhost:6379

# Monitoring and Analytics
PROMETHEUS_PORT=9090
LOG_LEVEL=INFO

# Business Configuration
BUSINESS_NAME=NatPropTech
BUSINESS_LOCATION=Natal-RN, Parnamirim-RN
BUSINESS_PHONE=+55-84-99999-9999
BUSINESS_EMAIL=contato@natproptech.com

# Agent Behavior
MAX_CONVERSATION_LENGTH=50
AUTO_RESPONSE_TIMEOUT=2
HUMAN_HANDOFF_THRESHOLD=0.8
LEAD_SCORE_THRESHOLD=0.7

# Performance Settings
MAX_CONCURRENT_CONVERSATIONS=100
RESPONSE_CACHE_TTL=3600
ANALYSIS_CACHE_TTL=1800
EOF
    
    # Cria arquivo .env se não existir
    if [ ! -f .env ]; then
        cp .env.example .env
        print_warning "Arquivo .env criado. Configure suas chaves de API!"
    else
        print_success "Arquivo .env já existe"
    fi
}

# Função para configurar banco de dados
setup_database() {
    print_step "Configurando banco de dados..."
    
    cat > setup_database.py << 'EOF'
#!/usr/bin/env python3
"""
Setup do banco de dados NatPropTech
"""

import sqlite3
import os
from datetime import datetime

def create_database():
    """Cria estrutura do banco de dados"""
    
    db_path = "natproptech.db"
    
    # Remove banco existente se houver
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tabela de leads
    cursor.execute("""
        CREATE TABLE leads (
            id TEXT PRIMARY KEY,
            phone TEXT UNIQUE NOT NULL,
            name TEXT,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_contact TIMESTAMP,
            intent_score REAL DEFAULT 0.0,
            priority TEXT DEFAULT 'medium',
            budget_range_min REAL DEFAULT 0,
            budget_range_max REAL DEFAULT 0,
            preferred_neighborhoods TEXT,  -- JSON array
            property_types TEXT,  -- JSON array
            timeline TEXT DEFAULT 'no_rush',
            has_financing BOOLEAN,
            conversion_probability REAL DEFAULT 0.5
        )
    """)
    
    # Tabela de conversas
    cursor.execute("""
        CREATE TABLE conversations (
            id TEXT PRIMARY KEY,
            lead_id TEXT,
            phone TEXT NOT NULL,
            message TEXT NOT NULL,
            response TEXT,
            intent TEXT,
            confidence REAL DEFAULT 0.0,
            sentiment TEXT DEFAULT 'neutral',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lead_id) REFERENCES leads (id)
        )
    """)
    
    # Tabela de imóveis
    cursor.execute("""
        CREATE TABLE properties (
            id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            neighborhood TEXT NOT NULL,
            bedrooms INTEGER,
            bathrooms INTEGER,
            parking_spaces INTEGER,
            price REAL NOT NULL,
            area REAL NOT NULL,
            description TEXT,
            features TEXT,  -- JSON array
            images TEXT,  -- JSON array
            status TEXT DEFAULT 'available',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabela de analytics
    cursor.execute("""
        CREATE TABLE analytics (
            id TEXT PRIMARY KEY,
            date DATE NOT NULL,
            total_conversations INTEGER DEFAULT 0,
            total_leads INTEGER DEFAULT 0,
            high_priority_leads INTEGER DEFAULT 0,
            conversions INTEGER DEFAULT 0,
            response_time_avg REAL DEFAULT 0.0,
            satisfaction_score REAL DEFAULT 0.0
        )
    """)
    
    # Tabela de configurações
    cursor.execute("""
        CREATE TABLE settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            description TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insere configurações padrão
    cursor.execute("""
        INSERT INTO settings (key, value, description) VALUES
        ('max_conversation_length', '50', 'Máximo de mensagens por conversa'),
        ('auto_response_timeout', '2', 'Timeout para resposta automática (segundos)'),
        ('human_handoff_threshold', '0.8', 'Threshold para transferência para humano'),
        ('lead_score_threshold', '0.7', 'Score mínimo para qualificar lead'),
        ('business_hours_start', '08:00', 'Horário de início do expediente'),
        ('business_hours_end', '18:00', 'Horário de fim do expediente')
    """)
    
    conn.commit()
    conn.close()
    
    print("✅ Banco de dados criado com sucesso!")

if __name__ == "__main__":
    create_database()
EOF
    
    python setup_database.py
    print_success "Banco de dados configurado"
}

# Função para configurar webhook
setup_webhook() {
    print_step "Configurando webhook WhatsApp..."
    
    cat > webhook_handler.py << 'EOF'
#!/usr/bin/env python3
"""
Webhook handler para WhatsApp Business API
"""

from flask import Flask, request, jsonify
import hmac
import hashlib
import json
import asyncio
from datetime import datetime

# Importa nosso sistema
from minimax_natproptech_sales_orchestrator import NatPropTechSalesSystem
from natproptech_agentic_integration import WhatsAppBusinessIntegration

app = Flask(__name__)

# Initialize sales system
sales_system = NatPropTechSalesSystem()

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """Webhook endpoint para WhatsApp Business API"""
    
    if request.method == 'GET':
        # Verificação inicial do webhook
        verify_token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if verify_token == 'natproptech_verify_token':
            return challenge
        else:
            return 'Token de verificação inválido', 403
    
    elif request.method == 'POST':
        # Processa mensagem recebida
        try:
            data = request.get_json()
            
            if 'messages' in data.get('entry', [{}])[0].get('changes', [{}])[0].get('value', {}):
                message_info = data['entry'][0]['changes'][0]['value']
                
                if 'messages' in message_info:
                    for message in message_info['messages']:
                        phone = message['from']
                        text = message['text']['body'] if 'text' in message else ''
                        
                        # Processa mensagem com nosso sistema
                        result = asyncio.run(sales_system.handle_whatsapp_message(text, phone))
                        
                        # Log da interação
                        print(f"Processada mensagem de {phone}: {result}")
                
                return 'OK', 200
            else:
                return 'No messages found', 200
                
        except Exception as e:
            print(f"Erro no webhook: {e}")
            return 'Error', 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
EOF
    
    print_success "Webhook configurado"
}

# Função para configurar monitoramento
setup_monitoring() {
    print_step "Configurando sistema de monitoramento..."
    
    cat > monitoring_dashboard.py << 'EOF'
#!/usr/bin/env python3
"""
Dashboard de monitoramento NatPropTech
"""

import time
import json
import sqlite3
from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Template HTML do dashboard
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>NatPropTech - Monitor de Vendas Agênticas</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }
        .metric-card { background: white; border-radius: 8px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric-value { font-size: 2em; font-weight: bold; color: #3498db; }
        .metric-label { color: #666; }
        .chart-container { background: white; border-radius: 8px; padding: 20px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏡 NatPropTech - Monitor de Vendas Agênticas</h1>
        <p>Dashboard em tempo real - Última atualização: {{ current_time }}</p>
    </div>
    
    <div class="metrics">
        <div class="metric-card">
            <div class="metric-value">{{ total_leads }}</div>
            <div class="metric-label">Total de Leads</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{{ high_priority_leads }}</div>
            <div class="metric-label">Leads Alta Prioridade</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{{ conversations_today }}</div>
            <div class="metric-label">Conversas Hoje</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{{ avg_response_time }}</div>
            <div class="metric-label">Tempo Médio Resposta</div>
        </div>
    </div>
    
    <div class="chart-container">
        <h3>Conversas por Hora</h3>
        <canvas id="conversationsChart"></canvas>
    </div>
    
    <script>
        // Dados para o gráfico
        const conversationsData = {{ conversations_data|tojson }};
        
        const ctx = document.getElementById('conversationsChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: conversationsData.labels,
                datasets: [{
                    label: 'Conversas',
                    data: conversationsData.values,
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.2)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Dashboard principal"""
    
    # Dados mockados (implementar coleta real dos dados)
    data = {
        'total_leads': 156,
        'high_priority_leads': 23,
        'conversations_today': 89,
        'avg_response_time': '2.3s',
        'conversations_data': {
            'labels': ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00'],
            'values': [5, 8, 12, 6, 4, 9, 11]
        }
    }
    
    return render_template_string(
        DASHBOARD_TEMPLATE,
        current_time=datetime.now().strftime('%d/%m/%Y %H:%M'),
        **data
    )

@app.route('/api/metrics')
def get_metrics():
    """API para métricas em JSON"""
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'metrics': {
            'total_leads': 156,
            'high_priority_leads': 23,
            'conversations_today': 89,
            'conversion_rate': 0.185,
            'avg_response_time': 2.3,
            'satisfaction_score': 4.7
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
EOF
    
    print_success "Sistema de monitoramento configurado"
}

# Função para criar scripts de inicialização
setup_startup_scripts() {
    print_step "Criando scripts de inicialização..."
    
    # Script para iniciar todos os serviços
    cat > start_all.sh << 'EOF'
#!/bin/bash
echo "🚀 Iniciando NatPropTech - Sistema de Vendas Agênticas"

# Ativa ambiente virtual
source natproptech_env/bin/activate

# Inicia serviços em background
nohup python webhook_handler.py > webhook.log 2>&1 &
WEBHOOK_PID=$!

nohup python monitoring_dashboard.py > monitoring.log 2>&1 &
MONITORING_PID=$!

echo "✅ Serviços iniciados:"
echo "   - Webhook: PID $WEBHOOK_PID (porta 5000)"
echo "   - Monitoring: PID $MONITORING_PID (porta 3000)"

echo "📊 Acesse o dashboard em: http://localhost:3000"
echo "🔧 Configure o webhook em: http://localhost:5000/webhook"

# Mantém script rodando
wait
EOF
    
    chmod +x start_all.sh
    
    # Script para parar todos os serviços
    cat > stop_all.sh << 'EOF'
#!/bin/bash
echo "🛑 Parando NatPropTech - Sistema de Vendas Agênticas"

# Mata processos
pkill -f webhook_handler.py
pkill -f monitoring_dashboard.py

echo "✅ Serviços parados"
EOF
    
    chmod +x stop_all.sh
    
    # Script de teste
    cat > test_system.py << 'EOF'
#!/usr/bin/env python3
"""
Teste do sistema NatPropTech
"""

import asyncio
from natproptech_agentic_integration import NatPropTechAgent
from minimax_natproptech_sales_orchestrator import NatPropTechSalesSystem

async def test_agent():
    """Testa agente básico"""
    print("🧪 Testando NatPropTech Agent...")
    
    agent = NatPropTechAgent(
        openai_api_key="test-key",
        whatsapp_config={"test": "config"}
    )
    
    result = await agent.process_whatsapp_message(
        "Olá, estou procurando um apartamento", 
        "+5584999999999"
    )
    
    print(f"✅ Resposta do agent: {result['response']}")
    return True

async def test_sales_system():
    """Testa sistema de vendas"""
    print("🧪 Testando Sales Orchestrator...")
    
    system = NatPropTechSalesSystem()
    
    result = await system.handle_whatsapp_message(
        "Meu orçamento é de 500 mil", 
        "+5584999999999"
    )
    
    print(f"✅ Resposta do sistema: {result['agent_response']}")
    return True

async def run_tests():
    """Executa todos os testes"""
    try:
        await test_agent()
        await test_sales_system()
        print("✅ Todos os testes passaram!")
        return True
    except Exception as e:
        print(f"❌ Erro nos testes: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(run_tests())
    exit(0 if success else 1)
EOF
    
    chmod +x test_system.py
    
    print_success "Scripts de inicialização criados"
}

# Função principal de instalação
main() {
    echo "🏗️ Iniciando instalação..."
    
    # Verifica se Python está instalado
    if ! command_exists python3; then
        print_error "Python 3 não encontrado. Instale Python 3.9+ primeiro."
        exit 1
    fi
    
    # Verifica se pip está instalado
    if ! command_exists pip; then
        print_error "pip não encontrado. Instale pip primeiro."
        exit 1
    fi
    
    # Cria ambiente virtual
    print_step "Criando ambiente virtual..."
    python3 -m venv $VENV_NAME
    source $VENV_NAME/bin/activate
    
    # Atualiza pip
    pip install --upgrade pip
    
    # Executa configuração
    install_python_dependencies
    setup_environment
    setup_database
    setup_webhook
    setup_monitoring
    setup_startup_scripts
    
    print_success "🎉 Instalação concluída!"
    echo ""
    echo "📋 Próximos passos:"
    echo "1. Configure suas chaves de API no arquivo .env"
    echo "2. Configure o webhook do WhatsApp Business API"
    echo "3. Execute ./test_system.py para testar"
    echo "4. Execute ./start_all.sh para iniciar os serviços"
    echo ""
    echo "🌐 URLs importantes:"
    echo "   - Dashboard: http://localhost:3000"
    echo "   - Webhook: http://localhost:5000/webhook"
    echo "   - API Metrics: http://localhost:3000/api/metrics"
    echo ""
    echo "📚 Documentação completa em:"
    echo "   - natproptech_agentic_integration.py"
    echo "   - minimax_natproptech_sales_orchestrator.py"
    echo ""
    echo "💡 Para suporte: contato@natproptech.com"
}

# Executa instalação se chamado diretamente
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi