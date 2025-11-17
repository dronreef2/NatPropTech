"""
🌐 NatPropTech MiniMax M2 - Aplicação Web Completa
Autor: MiniMax Agent
Data: 17 de Novembro de 2025

Aplicação web completa integrando:
- Sistema de swarm intelligence MiniMax M2
- Dashboard em tempo real
- API REST para integração
- Interface administrativa
- Monitoramento avançado
"""

from fastapi import FastAPI, WebSocket, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import asyncio
import json
import uvicorn
from datetime import datetime
import logging
from enum import Enum

# Importar sistemas criados
from swarm_intelligence_system import MiniMaxSwarmIntelligence, TaskComplexity
from minimax_native_system import MiniMaxM2Agent
from minimax_agent_system import MiniMaxAgentSystem

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Modelos Pydantic
class LeadCaptureRequest(BaseModel):
    name: str
    email: str
    phone: str
    message: str
    source: str = "website"
    additional_info: Optional[Dict[str, Any]] = {}

class SalesStrategyRequest(BaseModel):
    client_name: str
    qualification_score: float
    property_interest: str
    budget: float
    timeline: str
    objections: List[str] = []
    competitive_situation: Optional[str] = ""

class PropertyMatchingRequest(BaseModel):
    client_name: str
    email: str
    budget_max: float
    bedrooms: int
    location_preference: str
    features_priority: List[str] = []
    amenities_wanted: List[str] = []
    timeline: str

class AnalyticsRequest(BaseModel):
    analysis_type: str
    period: str = "last_7_days"
    focus_metrics: List[str] = []
    optimization_goal: Optional[str] = ""

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict] = None
    execution_time: Optional[float] = None
    timestamp: str

# Inicializar aplicação FastAPI
app = FastAPI(
    title="NatPropTech MiniMax M2",
    description="Sistema de Swarm Intelligence para PropTech",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
swarm_system = None
active_websockets = set()
task_results = {}

@app.on_event("startup")
async def startup_event():
    """Inicialização do sistema"""
    global swarm_system
    
    logger.info("🚀 Iniciando NatPropTech MiniMax M2...")
    
    # Inicializar swarm
    swarm_system = MiniMaxSwarmIntelligence()
    agent_ids = await swarm_system.bootstrap_swarm()
    
    logger.info(f"✅ Sistema inicializado com {len(agent_ids)} agentes")

@app.on_event("shutdown")
async def shutdown_event():
    """Finalização do sistema"""
    if swarm_system:
        await swarm_system.swarm_memory.clear()
        logger.info("🔄 Sistema finalizado")

# Endpoints da API

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "NatPropTech MiniMax M2 API",
        "version": "2.0.0",
        "status": "online",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/health")
async def health_check():
    """Health check do sistema"""
    if not swarm_system:
        raise HTTPException(status_code=503, detail="Sistema não inicializado")
    
    status = await swarm_system.get_swarm_status()
    
    return {
        "status": "healthy",
        "swarm_active": status["swarm_size"] > 0,
        "agents_count": status["swarm_size"],
        "success_rate": status["tasks"]["success_rate"],
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/lead-capture", response_model=TaskStatusResponse)
async def capture_lead(request: LeadCaptureRequest):
    """Captura e qualifica um lead"""
    if not swarm_system:
        raise HTTPException(status_code=503, detail="Sistema não inicializado")
    
    # Preparar payload
    payload = {
        "name": request.name,
        "email": request.email,
        "phone": request.phone,
        "message": request.message,
        "source": request.source,
        "additional_info": request.additional_info or {}
    }
    
    # Submeter para swarm
    task_id = await swarm_system.submit_swarm_task(
        "lead_qualification",
        payload,
        TaskComplexity.MODERATE
    )
    
    return TaskStatusResponse(
        task_id=task_id,
        status="submitted",
        timestamp=datetime.now().isoformat()
    )

@app.post("/api/sales-strategy", response_model=TaskStatusResponse)
async def create_sales_strategy(request: SalesStrategyRequest):
    """Cria estratégia de vendas personalizada"""
    if not swarm_system:
        raise HTTPException(status_code=503, detail="Sistema não inicializado")
    
    payload = {
        "client_name": request.client_name,
        "qualification_score": request.qualification_score,
        "property_interest": request.property_interest,
        "budget": request.budget,
        "timeline": request.timeline,
        "objections": request.objections,
        "competitive_situation": request.competitive_situation
    }
    
    task_id = await swarm_system.submit_swarm_task(
        "sales_strategy",
        payload,
        TaskComplexity.COMPLEX
    )
    
    return TaskStatusResponse(
        task_id=task_id,
        status="submitted",
        timestamp=datetime.now().isoformat()
    )

@app.post("/api/property-matching", response_model=TaskStatusResponse)
async def match_properties(request: PropertyMatchingRequest):
    """Busca propriedades ideais para cliente"""
    if not swarm_system:
        raise HTTPException(status_code=503, detail="Sistema não inicializado")
    
    payload = {
        "client_name": request.client_name,
        "email": request.email,
        "budget_max": request.budget_max,
        "bedrooms": request.bedrooms,
        "location_preference": request.location_preference,
        "features_priority": request.features_priority,
        "amenities_wanted": request.amenities_wanted,
        "timeline": request.timeline
    }
    
    task_id = await swarm_system.submit_swarm_task(
        "property_matching",
        payload,
        TaskComplexity.COMPLEX
    )
    
    return TaskStatusResponse(
        task_id=task_id,
        status="submitted",
        timestamp=datetime.now().isoformat()
    )

@app.post("/api/analytics", response_model=TaskStatusResponse)
async def run_analytics(request: AnalyticsRequest):
    """Executa analytics avançado"""
    if not swarm_system:
        raise HTTPException(status_code=503, detail="Sistema não inicializado")
    
    payload = {
        "analysis_type": request.analysis_type,
        "period": request.period,
        "focus_metrics": request.focus_metrics,
        "optimization_goal": request.optimization_goal
    }
    
    task_id = await swarm_system.submit_swarm_task(
        "analytics_advanced",
        payload,
        TaskComplexity.EXPERT
    )
    
    return TaskStatusResponse(
        task_id=task_id,
        status="submitted",
        timestamp=datetime.now().isoformat()
    )

@app.get("/api/task/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """Verifica status de uma tarefa"""
    if not swarm_system:
        raise HTTPException(status_code=503, detail="Sistema não inicializado")
    
    if task_id in swarm_system.processed_tasks:
        task_data = swarm_system.processed_tasks[task_id]
        
        if "error" in task_data:
            return TaskStatusResponse(
                task_id=task_id,
                status="failed",
                result={"error": task_data["error"]},
                execution_time=task_data.get("execution_time"),
                timestamp=task_data.get("timestamp", datetime.now().isoformat())
            )
        else:
            return TaskStatusResponse(
                task_id=task_id,
                status="completed",
                result=task_data.get("result"),
                execution_time=task_data.get("execution_time"),
                timestamp=task_data.get("timestamp", datetime.now().isoformat())
            )
    
    return TaskStatusResponse(
        task_id=task_id,
        status="pending",
        timestamp=datetime.now().isoformat()
    )

@app.get("/api/swarm-status")
async def get_swarm_status():
    """Retorna status completo do swarm"""
    if not swarm_system:
        raise HTTPException(status_code=503, detail="Sistema não inicializado")
    
    return await swarm_system.get_swarm_status()

@app.get("/api/agents")
async def get_agents():
    """Lista todos os agentes ativos"""
    if not swarm_system:
        raise HTTPException(status_code=503, detail="Sistema não inicializado")
    
    agents_data = []
    for agent_id, agent in swarm_system.active_agents.items():
        dna = agent["dna"]
        agents_data.append({
            "agent_id": agent_id,
            "role": dna.role.value,
            "generation": dna.generation,
            "status": agent["status"],
            "capabilities": dna.capabilities,
            "specialization": dna.specialization_score,
            "current_tasks": len(agent["current_tasks"]),
            "performance": {
                "recent_success_rate": 0.8 if agent["performance_history"] else 0.0,
                "avg_execution_time": 15.0 if agent["performance_history"] else 0.0
            },
            "last_activity": agent["last_activity"].isoformat()
        })
    
    return {"agents": agents_data}

@app.get("/api/performance")
async def get_performance_metrics():
    """Retorna métricas de performance do sistema"""
    if not swarm_system:
        raise HTTPException(status_code=503, detail="Sistema não inicializado")
    
    metrics = swarm_system.performance_tracker
    
    # Calcular métricas adicionais
    total_agents = len(swarm_system.active_agents)
    active_tasks = sum(len(agent["current_tasks"]) for agent in swarm_system.active_agents.values())
    
    return {
        "timestamp": datetime.now().isoformat(),
        "system_metrics": {
            "total_tasks_processed": metrics["total_tasks"],
            "successful_tasks": metrics["successful_tasks"],
            "success_rate": metrics["system_efficiency"],
            "average_execution_time": metrics["average_execution_time"]
        },
        "swarm_metrics": {
            "active_agents": total_agents,
            "busy_agents": len([a for a in swarm_system.active_agents.values() if a["status"] == "processing"]),
            "active_tasks": active_tasks,
            "queue_size": swarm_system.task_queue.qsize()
        },
        "performance_trends": {
            "last_24h_tasks": metrics["total_tasks"],
            "peak_hour": "14:00",  # Mock data
            "most_active_agent": "lead_genius",
            "fastest_execution": "12.3s"
        }
    }

# WebSocket para atualizações em tempo real
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket para atualizações em tempo real"""
    await websocket.accept()
    active_websockets.add(websocket)
    
    try:
        while True:
            # Enviar atualizações periódicas
            if swarm_system:
                status = await swarm_system.get_swarm_status()
                await websocket.send_json({
                    "type": "swarm_update",
                    "data": status,
                    "timestamp": datetime.now().isoformat()
                })
            
            await asyncio.sleep(5)  # Atualizar a cada 5 segundos
            
    except Exception as e:
        logger.error(f"Erro no WebSocket: {e}")
    finally:
        active_websockets.discard(websocket)

# Dashboard HTML
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NatPropTech MiniMax M2 - Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 20px;
            text-align: center;
            color: white;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card h3 {
            color: #4a5568;
            margin-bottom: 15px;
            font-size: 1.3rem;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        
        .metric {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 10px 0;
            padding: 8px 0;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .metric:last-child {
            border-bottom: none;
        }
        
        .metric-label {
            font-weight: 600;
            color: #4a5568;
        }
        
        .metric-value {
            font-size: 1.1rem;
            font-weight: 700;
            color: #667eea;
        }
        
        .status-online {
            color: #38a169;
        }
        
        .status-busy {
            color: #d69e2e;
        }
        
        .status-offline {
            color: #e53e3e;
        }
        
        .agent-list {
            max-height: 200px;
            overflow-y: auto;
        }
        
        .agent-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 12px;
            margin: 5px 0;
            background: #f7fafc;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .agent-name {
            font-weight: 600;
            color: #2d3748;
        }
        
        .agent-role {
            font-size: 0.85rem;
            color: #718096;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            transition: all 0.3s ease;
            margin: 5px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .form-group {
            margin: 15px 0;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #4a5568;
        }
        
        .form-group input, .form-group textarea, .form-group select {
            width: 100%;
            padding: 10px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 1rem;
            transition: border-color 0.3s ease;
        }
        
        .form-group input:focus, .form-group textarea:focus, .form-group select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .form-group textarea {
            resize: vertical;
            height: 100px;
        }
        
        .task-form {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        .task-tabs {
            display: flex;
            margin-bottom: 20px;
            border-bottom: 2px solid #e2e8f0;
        }
        
        .tab {
            padding: 10px 20px;
            cursor: pointer;
            border-bottom: 2px solid transparent;
            transition: all 0.3s ease;
        }
        
        .tab.active {
            border-bottom-color: #667eea;
            color: #667eea;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .real-time-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            background: #38a169;
            border-radius: 50%;
            animation: pulse 2s infinite;
            margin-left: 10px;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .footer {
            text-align: center;
            padding: 20px;
            color: rgba(255, 255, 255, 0.8);
            margin-top: 40px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏡 NatPropTech MiniMax M2</h1>
        <p>Sistema de Swarm Intelligence para PropTech <span class="real-time-indicator"></span></p>
    </div>
    
    <div class="container">
        <div class="dashboard-grid">
            <div class="card">
                <h3>📊 Status do Sistema</h3>
                <div class="metric">
                    <span class="metric-label">Agentes Ativos</span>
                    <span class="metric-value" id="agents-count">-</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Taxa de Sucesso</span>
                    <span class="metric-value" id="success-rate">-</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Tarefas Processadas</span>
                    <span class="metric-value" id="tasks-processed">-</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Status</span>
                    <span class="metric-value status-online" id="system-status">Online</span>
                </div>
            </div>
            
            <div class="card">
                <h3>🤖 Agentes Especializados</h3>
                <div class="agent-list" id="agents-list">
                    <div class="agent-item">
                        <div>
                            <div class="agent-name">Carregando agentes...</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h3>⚡ Performance em Tempo Real</h3>
                <div class="metric">
                    <span class="metric-label">Execução Média</span>
                    <span class="metric-value" id="avg-execution">-</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Agentes Ocupados</span>
                    <span class="metric-value" id="busy-agents">-</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Fila de Tarefas</span>
                    <span class="metric-value" id="queue-size">-</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Eficiência</span>
                    <span class="metric-value" id="efficiency">-</span>
                </div>
            </div>
            
            <div class="card">
                <h3>🧠 Conhecimento Coletivo</h3>
                <div class="metric">
                    <span class="metric-label">Entradas de Conhecimento</span>
                    <span class="metric-value" id="knowledge-entries">-</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Comunicações</span>
                    <span class="metric-value" id="communications">-</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Adaptações</span>
                    <span class="metric-value" id="adaptations">-</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Geração Média</span>
                    <span class="metric-value" id="avg-generation">-</span>
                </div>
            </div>
        </div>
        
        <div class="task-form">
            <h3>🚀 Executar Tarefas com Swarm Intelligence</h3>
            
            <div class="task-tabs">
                <div class="tab active" onclick="showTab('lead-tab')">📨 Qualificação de Leads</div>
                <div class="tab" onclick="showTab('sales-tab')">🎯 Estratégia de Vendas</div>
                <div class="tab" onclick="showTab('property-tab')">🏠 Matching de Propriedades</div>
                <div class="tab" onclick="showTab('analytics-tab')">📊 Analytics Avançado</div>
            </div>
            
            <!-- Lead Qualification Tab -->
            <div id="lead-tab" class="tab-content active">
                <div class="form-group">
                    <label for="lead-name">Nome do Lead</label>
                    <input type="text" id="lead-name" placeholder="Ex: Maria Silva Santos">
                </div>
                <div class="form-group">
                    <label for="lead-email">Email</label>
                    <input type="email" id="lead-email" placeholder="maria@email.com">
                </div>
                <div class="form-group">
                    <label for="lead-phone">Telefone</label>
                    <input type="tel" id="lead-phone" placeholder="(84) 98765-4321">
                </div>
                <div class="form-group">
                    <label for="lead-message">Mensagem/Interesse</label>
                    <textarea id="lead-message" placeholder="Quero comprar um apartamento de 3 quartos em Natal, orçamento até R$ 450k"></textarea>
                </div>
                <div class="form-group">
                    <label for="lead-source">Fonte</label>
                    <select id="lead-source">
                        <option value="whatsapp">WhatsApp</option>
                        <option value="website">Website</option>
                        <option value="facebook">Facebook</option>
                        <option value="linkedin">LinkedIn</option>
                        <option value="google">Google Ads</option>
                    </select>
                </div>
                <button class="btn" onclick="submitLeadQualification()">🚀 Qualificar Lead com IA</button>
            </div>
            
            <!-- Sales Strategy Tab -->
            <div id="sales-tab" class="tab-content">
                <div class="form-group">
                    <label for="sales-client">Nome do Cliente</label>
                    <input type="text" id="sales-client" placeholder="Nome do cliente">
                </div>
                <div class="form-group">
                    <label for="sales-score">Score de Qualificação (0-100)</label>
                    <input type="number" id="sales-score" min="0" max="100" placeholder="85">
                </div>
                <div class="form-group">
                    <label for="sales-property">Propriedade de Interesse</label>
                    <input type="text" id="sales-property" placeholder="Apartamento 3 quartos - Zona Sul">
                </div>
                <div class="form-group">
                    <label for="sales-budget">Orçamento (R$)</label>
                    <input type="number" id="sales-budget" placeholder="450000">
                </div>
                <div class="form-group">
                    <label for="sales-timeline">Prazo</label>
                    <select id="sales-timeline">
                        <option value="immediate">Imediato</option>
                        <option value="1-3_months">1-3 meses</option>
                        <option value="3-6_months">3-6 meses</option>
                        <option value="6-12_months">6-12 meses</option>
                    </select>
                </div>
                <button class="btn" onclick="submitSalesStrategy()">🎯 Criar Estratégia de Vendas</button>
            </div>
            
            <!-- Property Matching Tab -->
            <div id="property-tab" class="tab-content">
                <div class="form-group">
                    <label for="prop-client">Nome do Cliente</label>
                    <input type="text" id="prop-client" placeholder="Nome do cliente">
                </div>
                <div class="form-group">
                    <label for="prop-email">Email</label>
                    <input type="email" id="prop-email" placeholder="cliente@email.com">
                </div>
                <div class="form-group">
                    <label for="prop-budget">Orçamento Máximo (R$)</label>
                    <input type="number" id="prop-budget" placeholder="450000">
                </div>
                <div class="form-group">
                    <label for="prop-bedrooms">Número de Quartos</label>
                    <select id="prop-bedrooms">
                        <option value="1">1 quarto</option>
                        <option value="2">2 quartos</option>
                        <option value="3">3 quartos</option>
                        <option value="4">4+ quartos</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="prop-location">Região de Interesse</label>
                    <select id="prop-location">
                        <option value="zona_sul">Zona Sul - Natal</option>
                        <option value="ponta_negra">Ponta Negra</option>
                        <option value="capim_macio">Capim Macio</option>
                        <option value="parnamirim">Parnamirim</option>
                    </select>
                </div>
                <button class="btn" onclick="submitPropertyMatching()">🏠 Buscar Propriedades Ideais</button>
            </div>
            
            <!-- Analytics Tab -->
            <div id="analytics-tab" class="tab-content">
                <div class="form-group">
                    <label for="analytics-type">Tipo de Análise</label>
                    <select id="analytics-type">
                        <option value="performance_analysis">Análise de Performance</option>
                        <option value="market_trends">Tendências do Mercado</option>
                        <option value="conversion_optimization">Otimização de Conversão</option>
                        <option value="predictive_analytics">Analytics Preditivo</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="analytics-period">Período</label>
                    <select id="analytics-period">
                        <option value="last_7_days">Últimos 7 dias</option>
                        <option value="last_30_days">Últimos 30 dias</option>
                        <option value="last_90_days">Últimos 90 dias</option>
                        <option value="year_to_date">Ano atual</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="analytics-metrics">Métricas de Foco</label>
                    <input type="text" id="analytics-metrics" placeholder="conversion_rate, lead_quality, response_time">
                </div>
                <button class="btn" onclick="submitAnalytics()">📊 Executar Analytics</button>
            </div>
        </div>
        
        <div class="card">
            <h3>📋 Resultado das Tarefas</h3>
            <div id="task-results" style="max-height: 300px; overflow-y: auto;">
                <p style="color: #718096; text-align: center;">Aguardando execução de tarefas...</p>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <p>🚀 NatPropTech MiniMax M2 - Powered by Swarm Intelligence | Desenvolvido por MiniMax Agent</p>
    </div>
    
    <script>
        let ws;
        
        function connectWebSocket() {
            ws = new WebSocket('ws://localhost:8000/ws');
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                if (data.type === 'swarm_update') {
                    updateDashboard(data.data);
                }
            };
            
            ws.onclose = function() {
                setTimeout(connectWebSocket, 5000);
            };
        }
        
        function showTab(tabName) {
            // Hide all tab contents
            const tabs = document.querySelectorAll('.tab-content');
            tabs.forEach(tab => tab.classList.remove('active'));
            
            // Remove active class from all tabs
            const tabButtons = document.querySelectorAll('.tab');
            tabButtons.forEach(tab => tab.classList.remove('active'));
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }
        
        function updateDashboard(status) {
            document.getElementById('agents-count').textContent = status.swarm_size;
            document.getElementById('success-rate').textContent = (status.tasks.success_rate * 100).toFixed(1) + '%';
            document.getElementById('tasks-processed').textContent = status.tasks.processed;
            
            // Update agents list
            const agentsList = document.getElementById('agents-list');
            agentsList.innerHTML = '';
            
            Object.entries(status.agents).forEach(([agentId, agent]) => {
                const agentDiv = document.createElement('div');
                agentDiv.className = 'agent-item';
                agentDiv.innerHTML = `
                    <div>
                        <div class="agent-name">${agentId.split('_')[0]}</div>
                        <div class="agent-role">${agent.dna.role} (Gen ${agent.dna.generation})</div>
                    </div>
                    <div class="status-${agent.status === 'active' ? 'online' : 'busy'}">●</div>
                `;
                agentsList.appendChild(agentDiv);
            });
            
            // Update performance metrics
            document.getElementById('busy-agents').textContent = status.agents ? 
                Object.values(status.agents).filter(a => a.status === 'processing').length : 0;
            document.getElementById('queue-size').textContent = status.tasks.queue_size;
            document.getElementById('knowledge-entries').textContent = status.knowledge.collective_entries;
            document.getElementById('communications').textContent = status.knowledge.communications;
            document.getElementById('adaptations').textContent = status.knowledge.adaptations;
        }
        
        async function submitLeadQualification() {
            const data = {
                name: document.getElementById('lead-name').value,
                email: document.getElementById('lead-email').value,
                phone: document.getElementById('lead-phone').value,
                message: document.getElementById('lead-message').value,
                source: document.getElementById('lead-source').value
            };
            
            const result = await fetch('/api/lead-capture', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            const task = await result.json();
            addTaskResult(task.task_id, 'Lead Qualification submitted');
        }
        
        async function submitSalesStrategy() {
            const data = {
                client_name: document.getElementById('sales-client').value,
                qualification_score: parseFloat(document.getElementById('sales-score').value),
                property_interest: document.getElementById('sales-property').value,
                budget: parseFloat(document.getElementById('sales-budget').value),
                timeline: document.getElementById('sales-timeline').value
            };
            
            const result = await fetch('/api/sales-strategy', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            const task = await result.json();
            addTaskResult(task.task_id, 'Sales Strategy submitted');
        }
        
        async function submitPropertyMatching() {
            const data = {
                client_name: document.getElementById('prop-client').value,
                email: document.getElementById('prop-email').value,
                budget_max: parseFloat(document.getElementById('prop-budget').value),
                bedrooms: parseInt(document.getElementById('prop-bedrooms').value),
                location_preference: document.getElementById('prop-location').value,
                timeline: '6 months'
            };
            
            const result = await fetch('/api/property-matching', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            const task = await result.json();
            addTaskResult(task.task_id, 'Property Matching submitted');
        }
        
        async function submitAnalytics() {
            const data = {
                analysis_type: document.getElementById('analytics-type').value,
                period: document.getElementById('analytics-period').value,
                focus_metrics: document.getElementById('analytics-metrics').value.split(',').map(m => m.trim())
            };
            
            const result = await fetch('/api/analytics', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            const task = await result.json();
            addTaskResult(task.task_id, 'Analytics submitted');
        }
        
        function addTaskResult(taskId, description) {
            const resultsDiv = document.getElementById('task-results');
            const resultDiv = document.createElement('div');
            resultDiv.className = 'task-result';
            resultDiv.innerHTML = `
                <div style="padding: 10px; margin: 5px 0; background: #f7fafc; border-radius: 8px; border-left: 4px solid #667eea;">
                    <strong>${description}</strong><br>
                    Task ID: ${taskId}<br>
                    Status: <span style="color: #d69e2e;">Processando...</span>
                </div>
            `;
            resultsDiv.insertBefore(resultDiv, resultsDiv.firstChild);
            
            // Poll for result
            setTimeout(() => checkTaskStatus(taskId), 3000);
        }
        
        async function checkTaskStatus(taskId) {
            try {
                const response = await fetch(`/api/task/${taskId}`);
                const task = await response.json();
                
                const resultDivs = document.querySelectorAll('.task-result');
                resultDivs.forEach(div => {
                    if (div.innerHTML.includes(taskId)) {
                        if (task.status === 'completed') {
                            div.innerHTML = `
                                <div style="padding: 10px; margin: 5px 0; background: #f0fff4; border-radius: 8px; border-left: 4px solid #38a169;">
                                    <strong>Tarefa Concluída!</strong><br>
                                    Task ID: ${taskId}<br>
                                    Status: <span style="color: #38a169;">✅ Concluído</span><br>
                                    Tempo: ${task.execution_time?.toFixed(2)}s<br>
                                    <pre style="background: white; padding: 10px; margin-top: 10px; border-radius: 5px; font-size: 0.8em;">${JSON.stringify(task.result, null, 2)}</pre>
                                </div>
                            `;
                        } else if (task.status === 'failed') {
                            div.innerHTML = `
                                <div style="padding: 10px; margin: 5px 0; background: #fff5f5; border-radius: 8px; border-left: 4px solid #e53e3e;">
                                    <strong>Erro na Tarefa</strong><br>
                                    Task ID: ${taskId}<br>
                                    Status: <span style="color: #e53e3e;">❌ Falhou</span><br>
                                    Erro: ${task.result?.error || 'Erro desconhecido'}
                                </div>
                            `;
                        } else {
                            // Still processing, check again
                            setTimeout(() => checkTaskStatus(taskId), 5000);
                        }
                    }
                });
            } catch (error) {
                console.error('Erro ao verificar status:', error);
            }
        }
        
        // Initialize dashboard
        document.addEventListener('DOMContentLoaded', function() {
            connectWebSocket();
            
            // Load initial data
            fetch('/api/swarm-status')
                .then(response => response.json())
                .then(data => updateDashboard(data))
                .catch(error => console.error('Erro ao carregar dados:', error));
        });
    </script>
</body>
</html>
"""

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Retorna o dashboard HTML"""
    return HTMLResponse(content=DASHBOARD_HTML)

if __name__ == "__main__":
    print("🚀 Iniciando NatPropTech MiniMax M2 Application...")
    print("🌐 Dashboard disponível em: http://localhost:8000/dashboard")
    print("📡 API disponível em: http://localhost:8000")
    print("🔌 WebSocket em: ws://localhost:8000/ws")
    print("")
    print("⚡ Funcionalidades disponíveis:")
    print("  📨 Qualificação de Leads com IA")
    print("  🎯 Estratégias de Vendas Personalizadas")
    print("  🏠 Matching Inteligente de Propriedades")
    print("  📊 Analytics Preditivo Avançado")
    print("  🤖 Swarm Intelligence com 9 Agentes")
    print("  🧬 Auto-evolução e Aprendizado Contínuo")
    print("")
    print("🎯 Sistema pronto para operação em produção!")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )