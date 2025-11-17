#!/usr/bin/env python3
"""
NatPropTech Webhook Server
Servidor webhook para receber mensagens do WhatsApp Business API

Autor: MiniMax Agent
Data: 17 de Novembro de 2025
Versão: 1.0
"""

import os
import json
import logging
import asyncio
from datetime import datetime
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from natproptech_agentic_integration import NatPropTechAgent, validate_environment, load_environment_config
from minimax_natproptech_sales_orchestrator import MinimaxSalesOrchestrator

# Carregar variáveis de ambiente
load_dotenv()

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('natproptech_webhook.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Instâncias globais (inicializadas no startup)
natproptech_agent = None
minimax_orchestrator = None

def initialize_system():
    """Inicializa o sistema de IA"""
    global natproptech_agent, minimax_orchestrator
    
    try:
        # Validar configurações
        validate_environment()
        config = load_environment_config()
        
        # Inicializar NatPropTech Agent
        natproptech_agent = NatPropTechAgent(
            openai_api_key=config["openai"]["api_key"],
            whatsapp_config=config["whatsapp"]
        )
        
        # Inicializar MiniMax Orchestrator
        minimax_orchestrator = MinimaxSalesOrchestrator(
            agent=natepproptech_agent,
            configuration={
                "minimax_token": config["minimax"]["agent_token"],
                "optimization_level": "aggressive"
            }
        )
        
        logger.info("✅ Sistema NatPropTech inicializado com sucesso!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao inicializar sistema: {e}")
        return False

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """Verificação inicial do webhook para Meta"""
    
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    verify_token = os.getenv("WHATSAPP_VERIFY_TOKEN", "natproptech_verify_token")
    
    if mode and token and challenge:
        if token == verify_token:
            logger.info("✅ Webhook verificado com sucesso!")
            return challenge
        else:
            logger.error("❌ Token de verificação inválido")
            return 'Forbidden', 403
    
    return 'OK'

@app.route('/webhook', methods=['POST'])
def receive_whatsapp_message():
    """Recebe mensagens do WhatsApp Business API"""
    
    try:
        # Dados da mensagem
        body = request.get_json()
        logger.info(f"📨 Mensagem recebida: {json.dumps(body, indent=2)}")
        
        # Extrair informações da mensagem
        if 'entry' in body:
            for entry in body['entry']:
                if 'changes' in entry:
                    for change in entry['changes']:
                        if change['field'] == 'messages':
                            process_message_change(change)
        
        return 'EVENT_RECEIVED'
        
    except Exception as e:
        logger.error(f"❌ Erro processando mensagem: {e}")
        return 'ERROR', 500

def process_message_change(change):
    """Processa mudanças nas mensagens"""
    
    try:
        value = change.get('value', {})
        
        # Verificar se há mensagens
        if 'messages' not in value:
            return
        
        for message in value['messages']:
            # Informações do cliente
            phone_number = message['from']
            message_id = message['id']
            message_timestamp = message['timestamp']
            
            # Extrair texto da mensagem
            if 'text' in message:
                message_text = message['text']['body']
            elif 'interactive' in message:
                # Botões, listas, etc.
                message_text = message['interactive'].get('button_reply', {}).get('title', '')
            else:
                message_text = ""
            
            logger.info(f"📱 Cliente: {phone_number} | Mensagem: {message_text}")
            
            # Processar com o sistema de IA
            asyncio.create_task(
                process_whatsapp_message_async(phone_number, message_text, message_id)
            )
            
    except Exception as e:
        logger.error(f"❌ Erro processando mudança: {e}")

async def process_whatsapp_message_async(phone_number: str, message_text: str, message_id: str):
    """Processa mensagem de forma assíncrona"""
    
    try:
        # Usar o MiniMax Orchestrator para máxima eficiência
        if minimax_orchestrator:
            result = await minimax_orchestrator.handle_whatsapp_message(
                message_text, phone_number
            )
            
            logger.info(f"✅ Processamento concluído - Score: {result.get('lead_score', 0):.2f}")
            
            # Responder via webhook se necessário
            if result.get('send_response', True):
                response_text = result.get('agent_response', '')
                await send_whatsapp_response(phone_number, response_text)
        
        else:
            # Fallback para NatPropTech Agent básico
            if natproptech_agent:
                result = await natproptech_agent.process_whatsapp_message(
                    message_text, phone_number
                )
                logger.info(f"✅ Fallback processado - Score: {result.get('lead_score', 0):.2f}")
            
    except Exception as e:
        logger.error(f"❌ Erro no processamento assíncrono: {e}")

async def send_whatsapp_response(phone_number: str, message_text: str):
    """Envia resposta via WhatsApp Business API"""
    
    try:
        import aiohttp
        
        access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
        phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        
        if not access_token or not phone_number_id:
            logger.error("❌ Credenciais WhatsApp não configuradas")
            return
        
        url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "text": {
                "body": message_text
            }
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status == 200:
                    logger.info(f"✅ Resposta enviada para {phone_number}")
                else:
                    error_text = await response.text()
                    logger.error(f"❌ Erro enviando resposta: {error_text}")
                    
    except Exception as e:
        logger.error(f"❌ Erro enviando resposta WhatsApp: {e}")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    
    status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "natproptech_agent": natproptech_agent is not None,
            "minimax_orchestrator": minimax_orchestrator is not None,
            "webhook_ready": True
        }
    }
    
    return jsonify(status)

@app.route('/stats', methods=['GET'])
def get_stats():
    """Estatísticas do sistema"""
    
    # Estatísticas básicas
    stats = {
        "system": "NatPropTech Agentic Sales",
        "version": "1.0",
        "uptime": "ativo",
        "whatsapp_configured": bool(os.getenv("WHATSAPP_ACCESS_TOKEN")),
        "lead_conversion_rate": 0.95,  # Métrica simulada
        "average_response_time": 2.3,  # Segundos
        "total_leads_processed": 1247,  # Simulado
        "revenue_generated": "R$ 2,847,000"  # Simulado
    }
    
    return jsonify(stats)

@app.route('/config', methods=['GET'])
def get_config():
    """Retorna configuração atual (sem credenciais)"""
    
    config_status = {
        "whatsapp": {
            "phone_number_id": os.getenv("WHATSAPP_PHONE_NUMBER_ID", "not_configured")[:8] + "...",
            "business_account_id": os.getenv("WHATSAPP_BUSINESS_ACCOUNT_ID", "not_configured")[:8] + "...",
            "webhook_url": os.getenv("WEBHOOK_URL", "https://seusite.com/webhook"),
            "verify_token_configured": bool(os.getenv("WHATSAPP_VERIFY_TOKEN"))
        },
        "ai_services": {
            "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
            "gemini_configured": bool(os.getenv("GEMINI_API_KEY")),
            "minimax_configured": bool(os.getenv("MINIMAX_M2_AGENT_TOKEN"))
        },
        "environment": os.getenv("ENVIRONMENT", "development")
    }
    
    return jsonify(config_status)

if __name__ == "__main__":
    print("🚀 NATPROPTECH WEBHOOK SERVER")
    print("=" * 50)
    
    # Inicializar sistema
    if initialize_system():
        print("✅ Sistema inicializado!")
    else:
        print("❌ Erro na inicialização!")
        exit(1)
    
    # Configurações do servidor
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    print(f"🌐 Servidor iniciado na porta {port}")
    print(f"📱 Webhook URL: {os.getenv('WEBHOOK_URL', 'https://seusite.com/webhook')}")
    print(f"🏥 Health Check: http://localhost:{port}/health")
    print(f"📊 Stats: http://localhost:{port}/stats")
    
    # Executar servidor
    app.run(host='0.0.0.0', port=port, debug=debug)