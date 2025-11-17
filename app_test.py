"""
🌐 NatPropTech MiniMax M2 - Aplicação Simplificada para Teste
Autor: MiniMax Agent
Data: 17 de Novembro de 2025
"""

import sys
sys.path.append('/workspace')

import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import asyncio
import json
from datetime import datetime

# Importar sistemas
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

# Configurar aplicação FastAPI
app = FastAPI(
    title="NatPropTech MiniMax M2",
    description="Plataforma de IA para Imobiliário - Sistema Integrado",
    version="1.0.0"
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
    version: str

class LeadCaptureRequest(BaseModel):
    name: str
    email: str
    phone: str
    message: str
    source: str = "website"

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
        version="1.0.0"
    )

@app.get("/dashboard")
async def dashboard():
    """Dashboard principal"""
    return {
        "title": "NatPropTech MiniMax M2 - Dashboard",
        "status": "Sistema Integrado Ativo",
        "features": [
            "🤖 Swarm Intelligence com 9 Agentes Especializados",
            "🧬 Auto-evolução e Aprendizado Contínuo",
            "🎯 Qualificação Inteligente de Leads",
            "📊 Analytics Preditivo Avançado",
            "🏠 Matching Inteligente de Propriedades",
            "💰 Estratégias de Vendas Otimizadas"
        ],
        "api_endpoints": {
            "health": "/",
            "lead_capture": "/api/lead-capture",
            "websocket": "/ws"
        }
    }

@app.post("/api/lead-capture")
async def capture_lead(request: LeadCaptureRequest):
    """Endpoint para captura de leads com IA"""
    try:
        # Simular processamento de lead
        lead_data = {
            "id": f"lead_{datetime.now().timestamp()}",
            "name": request.name,
            "email": request.email,
            "phone": request.phone,
            "message": request.message,
            "source": request.source,
            "timestamp": datetime.now().isoformat(),
            "status": "captured",
            "qualification_score": 0.8  # Simulado
        }
        
        return {
            "success": True,
            "message": "Lead capturado com sucesso!",
            "lead_id": lead_data["id"],
            "qualification_score": lead_data["qualification_score"],
            "next_actions": [
                "Enviar email de boas-vindas",
                "Agendar follow-up em 24h",
                "Classificar lead para time de vendas"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar lead: {str(e)}")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket para comunicação em tempo real"""
    await websocket.accept()
    
    try:
        while True:
            # Receber mensagem do cliente
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Processar e responder
            response = {
                "type": "response",
                "timestamp": datetime.now().isoformat(),
                "data": f"Recebido: {message.get('message', 'Mensagem vazia')}",
                "server_status": "active"
            }
            
            await websocket.send_text(json.dumps(response))
            
    except Exception as e:
        print(f"WebSocket error: {e}")

# Informações de inicialização
print("=" * 60)
print("🚀 NATPROPTECH MINIMAX M2 - SISTEMA INTEGRADO")
print("=" * 60)
print(f"✅ Swarm Intelligence: {'ATIVO' if SWARM_AVAILABLE else 'INATIVO'}")
print(f"✅ MiniMax Native: {'ATIVO' if MINIMAX_NATIVE_AVAILABLE else 'INATIVO'}")
print(f"✅ MiniMax Agent: {'ATIVO' if MINIMAX_AGENT_AVAILABLE else 'INATIVO'}")
print(f"✅ Gemini API: {'CONFIGURADO' if os.getenv('GEMINI_API_KEY') else 'NÃO CONFIGURADO'}")
print(f"✅ MiniMax API: {'CONFIGURADO' if os.getenv('MINIMAX_M2_AGENT_TOKEN') else 'NÃO CONFIGURADO'}")
print("=" * 60)
print("🌐 Dashboard: http://localhost:8000/dashboard")
print("📡 API: http://localhost:8000")
print("🔌 WebSocket: ws://localhost:8000/ws")
print("=" * 60)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)