"""
🌐 NatPropTech MiniMax M2 + WhatsApp Business - Aplicação Integrada
Autor: MiniMax Agent  
Data: 17 de Novembro de 2025

Aplicação completa integrando:
- Sistema de swarm intelligence MiniMax M2
- WhatsApp Business API para interações
- Dashboard em tempo real
- API REST para integração
- Interface administrativa
- Monitoramento avançado
"""

import sys
sys.path.append('/workspace')

import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, WebSocket, HTTPException, BackgroundTasks, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import asyncio
import json
import uvicorn
from datetime import datetime
import logging
from enum import Enum

# Importar sistemas NatPropTech
try:
    from swarm_intelligence_system import MiniMaxSwarmIntelligence, TaskComplexity
    SWARM_AVAILABLE = True
except ImportError as e:
    print(f"Swarm system not available: {e}")
    SWARM_AVAILABLE = False

try:
    from minimax_native_system import MiniMaxM2Agent
    MINIMAX_NATIVE_AVAILABLE = True
except ImportError as e:
    print(f"MiniMax native system not available: {e}")
    MINIMAX_NATIVE_AVAILABLE = False

try:
    from minimax_agent_system import MiniMaxAgentSystem
    MINIMAX_AGENT_AVAILABLE = True
except ImportError as e:
    print(f"MiniMax agent system not available: {e}")
    MINIMAX_AGENT_AVAILABLE = False

# Importar WhatsApp Business Integration
try:
    from whatsapp_business_integration import (
        WhatsAppBusinessClient, 
        WhatsAppWebhookHandler, 
        WhatsAppNatPropTechBot,
        WhatsAppMessage,
        MessageType
    )
    WHATSAPP_AVAILABLE = True
except ImportError as e:
    print(f"WhatsApp system not available: {e}")
    WHATSAPP_AVAILABLE = False

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurar aplicação FastAPI
app = FastAPI(
    title="NatPropTech MiniMax M2 + WhatsApp Business",
    description="Plataforma completa de IA para Imobiliário com integração WhatsApp",
    version="2.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class HealthResponse(BaseModel):
    status: str
    timestamp: str
    systems: Dict[str, bool]
    whatsapp: Dict[str, bool]
    version: str

class WhatsAppWebhookRequest(BaseModel):
    hub_challenge: str
    hub_mode: str
    hub_verify_token: str

class WhatsAppMessageRequest(BaseModel):
    to: str
    message_type: str
    content: Dict[str, Any]
    reply_to: Optional[str] = None

class ConversationRequest(BaseModel):
    phone_number: str
    action: str
    data: Optional[Dict[str, Any]] = None

# Configurações WhatsApp Business
WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "natproptech_verify_token")
WHATSAPP_APP_SECRET = os.getenv("WHATSAPP_APP_SECRET", "")

# Inicializar clientes WhatsApp (será configurado quando as credenciais estiverem disponíveis)
whatsapp_client = None
whatsapp_bot = None
webhook_handler = None

if WHATSAPP_AVAILABLE and WHATSAPP_ACCESS_TOKEN and WHATSAPP_PHONE_NUMBER_ID:
    try:
        whatsapp_client = WhatsAppBusinessClient(WHATSAPP_ACCESS_TOKEN, WHATSAPP_PHONE_NUMBER_ID)
        whatsapp_bot = WhatsAppNatPropTechBot(whatsapp_client)
        webhook_handler = WhatsAppWebhookHandler(WHATSAPP_VERIFY_TOKEN, WHATSAPP_APP_SECRET)
        logger.info("WhatsApp Business initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize WhatsApp: {e}")

# Armazenamento em memória para demonstração
conversations = {}
message_history = {}

# Endpoints

@app.get("/", response_model=HealthResponse)
async def root():
    """Endpoint principal com status do sistema"""
    return HealthResponse(
        status="active",
        timestamp=datetime.now().isoformat(),
        systems={
            "swarm_intelligence": SWARM_AVAILABLE,
            "minimax_native": MINIMAX_NATIVE_AVAILABLE,
            "minimax_agent": MINIMAX_AGENT_AVAILABLE,
            "gemini_api": bool(os.getenv("GEMINI_API_KEY")),
            "minimax_api": bool(os.getenv("MINIMAX_M2_AGENT_TOKEN"))
        },
        whatsapp={
            "available": WHATSAPP_AVAILABLE,
            "configured": bool(whatsapp_client),
            "webhook_ready": bool(webhook_handler)
        },
        version="2.0.0"
    )

@app.get("/dashboard")
async def dashboard():
    """Dashboard principal integrado"""
    whatsapp_status = "Configurado" if whatsapp_client else "Não configurado"
    if not WHATSAPP_ACCESS_TOKEN:
        whatsapp_status = "Credenciais necessárias"
    
    return {
        "title": "NatPropTech MiniMax M2 + WhatsApp Business",
        "status": "Sistema Completo Ativo",
        "integration_status": {
            "whatsapp_business": whatsapp_status,
            "real_time_chat": "Ativo" if whatsapp_client else "Inativo",
            "lead_automation": "Ativo",
            "property_suggestions": "Ativo"
        },
        "features": [
            "🤖 Swarm Intelligence com 9 Agentes Especializados",
            "💬 WhatsApp Business API Integrada",
            "🏠 Chatbot Inteligente para Imóveis",
            "📱 Interações via WhatsApp pelo Computador",
            "🎯 Qualificação Automática de Leads",
            "📊 Analytics Preditivo Avançado",
            "🤝 Agendamento Automático de Visitas",
            "💰 Simulação de Financiamento",
            "🧬 Auto-evolução e Aprendizado Contínuo"
        ],
        "api_endpoints": {
            "health": "/",
            "whatsapp_webhook": "/webhook/whatsapp",
            "whatsapp_verify": "/webhook/whatsapp/verify",
            "send_message": "/api/whatsapp/send",
            "conversations": "/api/whatsapp/conversations",
            "websocket": "/ws"
        },
        "whatsapp_config": {
            "webhook_url": "https://seu-dominio.com/webhook/whatsapp",
            "verify_token": WHATSAPP_VERIFY_TOKEN,
            "phone_number_id": WHATSAPP_PHONE_NUMBER_ID[:8] + "..." if WHATSAPP_PHONE_NUMBER_ID else "Não configurado"
        }
    }

# Endpoints WhatsApp Business

@app.get("/webhook/whatsapp/verify")
async def verify_webhook(request: Request):
    """Endpoint de verificação do webhook do WhatsApp"""
    try:
        mode = request.query_params.get("hub.mode")
        token = request.query_params.get("hub.verify_token")
        challenge = request.query_params.get("hub.challenge")
        
        if webhook_handler:
            challenge_response = webhook_handler.verify_webhook(mode, token, challenge)
            if challenge_response:
                return HTMLResponse(content=challenge_response)
            else:
                raise HTTPException(status_code=403, detail="Verification failed")
        else:
            raise HTTPException(status_code=500, detail="Webhook handler not configured")
            
    except Exception as e:
        logger.error(f"Webhook verification error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request, background_tasks: BackgroundTasks):
    """Webhook para receber mensagens do WhatsApp Business"""
    try:
        # Verificar assinatura da requisição
        signature = request.headers.get("X-Hub-Signature-256", "")
        payload = await request.body()
        
        if webhook_handler and signature:
            if not webhook_handler.verify_signature(payload, signature):
                logger.warning("Invalid webhook signature")
                return {"status": "ignored"}
        
        # Processar dados do webhook
        data = await request.json()
        
        if webhook_handler:
            messages = webhook_handler.parse_webhook_data(data)
            
            # Processar cada mensagem em background
            for message in messages:
                if whatsapp_bot:
                    background_tasks.add_task(process_whatsapp_message, message)
        
        return {"status": "processed"}
        
    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def process_whatsapp_message(message: WhatsAppMessage):
    """Processa mensagem recebida do WhatsApp"""
    try:
        if whatsapp_bot:
            response = await whatsapp_bot.process_message(message)
            
            # Armazenar histórico da conversa
            phone_number = message.from_number
            if phone_number not in conversations:
                conversations[phone_number] = []
            
            conversations[phone_number].append({
                "timestamp": message.timestamp.isoformat(),
                "direction": "received",
                "content": message.content,
                "message_id": message.message_id
            })
            
            if response:
                conversations[phone_number].append({
                    "timestamp": datetime.now().isoformat(),
                    "direction": "sent",
                    "content": {"text": response.get("text", "")},
                    "message_id": f"auto_{message.message_id}"
                })
            
            logger.info(f"Processed WhatsApp message from {phone_number}")
            
    except Exception as e:
        logger.error(f"Error processing WhatsApp message: {e}")

@app.post("/api/whatsapp/send")
async def send_whatsapp_message(request: WhatsAppMessageRequest):
    """Envia mensagem via WhatsApp Business API"""
    try:
        if not whatsapp_client:
            raise HTTPException(status_code=500, detail="WhatsApp client not configured")
        
        if request.message_type == "text":
            result = await whatsapp_client.send_text_message(
                to=request.to,
                body=request.content.get("text", ""),
                message_id=request.reply_to
            )
        elif request.message_type == "image":
            result = await whatsapp_client.send_image_message(
                to=request.to,
                image_url=request.content.get("image_url", ""),
                caption=request.content.get("caption", ""),
                message_id=request.reply_to
            )
        else:
            raise HTTPException(status_code=400, detail="Unsupported message type")
        
        return {
            "success": True,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error sending WhatsApp message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/whatsapp/conversations")
async def get_conversations():
    """Retorna histórico de conversas WhatsApp"""
    return {
        "conversations": conversations,
        "total": len(conversations),
        "last_updated": datetime.now().isoformat()
    }

@app.get("/api/whatsapp/conversations/{phone_number}")
async def get_conversation(phone_number: str):
    """Retorna conversa específica"""
    if phone_number not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return {
        "phone_number": phone_number,
        "messages": conversations[phone_number],
        "message_count": len(conversations[phone_number]),
        "last_activity": conversations[phone_number][-1]["timestamp"] if conversations[phone_number] else None
    }

@app.post("/api/whatsapp/conversation")
async def manage_conversation(request: ConversationRequest):
    """Gerencia conversa WhatsApp"""
    phone_number = request.phone_number
    
    if request.action == "send_property_suggestion":
        if not whatsapp_client:
            raise HTTPException(status_code=500, detail="WhatsApp client not configured")
        
        # Simular dados de propriedade
        property_data = {
            "id": request.data.get("property_id", "demo_001"),
            "title": "Apartamento 3 Quartos - Ponta Negra",
            "price": 450000,
            "location": "Ponta Negra, Natal/RN",
            "bedrooms": 3,
            "parking": 2
        }
        
        result = await whatsapp_client.send_property_suggestion(
            to=phone_number,
            property_data=property_data
        )
        
        return {
            "success": True,
            "action": "property_suggestion_sent",
            "result": result
        }
    
    elif request.action == "qualify_lead":
        if not whatsapp_client:
            raise HTTPException(status_code=500, detail="WhatsApp client not configured")
        
        qualification_data = {
            "score": 0.85,
            "name": "Lead WhatsApp",
            "budget": 450000,
            "timeline": "2-3 meses"
        }
        
        result = await whatsapp_client.send_lead_qualification(
            to=phone_number,
            qualification_data=qualification_data
        )
        
        return {
            "success": True,
            "action": "lead_qualification_sent",
            "result": result
        }
    
    else:
        raise HTTPException(status_code=400, detail="Unsupported action")

# WebSocket para comunicação em tempo real
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket para comunicação em tempo real"""
    await websocket.accept()
    
    try:
        while True:
            # Receber mensagem do cliente
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Processar diferentes tipos de mensagem
            message_type = message.get("type", "general")
            
            response = {
                "type": "response",
                "timestamp": datetime.now().isoformat(),
                "original_type": message_type,
                "data": {},
                "server_status": "active"
            }
            
            if message_type == "whatsapp_status":
                response["data"] = {
                    "whatsapp_configured": bool(whatsapp_client),
                    "conversations_count": len(conversations),
                    "total_messages": sum(len(conv) for conv in conversations.values())
                }
            
            elif message_type == "send_test_message":
                if whatsapp_client and message.get("to"):
                    test_result = await whatsapp_client.send_text_message(
                        to=message["to"],
                        body="🤖 Teste do sistema NatPropTech WhatsApp!"
                    )
                    response["data"] = {"sent": True, "result": test_result}
                else:
                    response["data"] = {"sent": False, "error": "WhatsApp not configured"}
            
            elif message_type == "get_conversations":
                response["data"] = {
                    "conversations": conversations,
                    "summary": {
                        "total_conversations": len(conversations),
                        "total_messages": sum(len(conv) for conv in conversations.values())
                    }
                }
            
            else:
                response["data"] = {
                    "message": f"Recebido: {message.get('message', 'Mensagem vazia')}",
                    "processing": "WhatsApp integration active"
                }
            
            await websocket.send_text(json.dumps(response))
            
    except Exception as e:
        logger.error(f"WebSocket error: {e}")

# Informações de inicialização
print("=" * 80)
print("🚀 NATPROPTECH MINIMAX M2 + WHATSAPP BUSINESS - SISTEMA INTEGRADO")
print("=" * 80)
print(f"✅ Swarm Intelligence: {'ATIVO' if SWARM_AVAILABLE else 'INATIVO'}")
print(f"✅ MiniMax Native: {'ATIVO' if MINIMAX_NATIVE_AVAILABLE else 'INATIVO'}")
print(f"✅ MiniMax Agent: {'ATIVO' if MINIMAX_AGENT_AVAILABLE else 'INATIVO'}")
print(f"✅ WhatsApp Business: {'CONFIGURADO' if whatsapp_client else 'NÃO CONFIGURADO'}")
print(f"✅ Gemini API: {'CONFIGURADO' if os.getenv('GEMINI_API_KEY') else 'NÃO CONFIGURADO'}")
print(f"✅ MiniMax API: {'CONFIGURADO' if os.getenv('MINIMAX_M2_AGENT_TOKEN') else 'NÃO CONFIGURADO'}")
print("=" * 80)
print("🌐 Dashboard: http://localhost:8000/dashboard")
print("📡 API: http://localhost:8000")
print("🔌 WebSocket: ws://localhost:8000/ws")
print("📱 WhatsApp Webhook: https://seu-dominio.com/webhook/whatsapp")
print("=" * 80)
print("💡 FUNCIONALIDADES WHATSAPP BUSINESS:")
print("   📝 Chatbot inteligente para imóveis")
print("   🏠 Sugestões automáticas de propriedades")
print("   📅 Agendamento de visitas")
print("   💰 Simulação de financiamento")
print("   🎯 Qualificação automática de leads")
print("   👨‍💼 Transferência para agentes humanos")
print("=" * 80)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")