"""
🚀 MiniMax M2 Agent Architecture - NatPropTech
Autor: MiniMax Agent
Data: 17 de Novembro de 2025

Sistema de IA Multi-Agente usando MiniMax-M2 API para automação completa do processo imobiliário.
"""

import asyncio
import json
import aiohttp
import base64
import jwt
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import google.generativeai as genai
from google.cloud import bigquery
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentStatus(Enum):
    IDLE = "idle"
    PROCESSING = "processing"  
    LEARNING = "learning"
    ERROR = "error"

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

@dataclass
class AgentContext:
    """Contexto persistente para cada agente"""
    agent_id: str
    name: str
    role: str
    capabilities: List[str]
    memory: Dict[str, Any]
    learning_patterns: List[Dict]
    performance_metrics: Dict[str, float]
    status: AgentStatus
    last_activity: datetime
    config: Dict[str, Any]

@dataclass 
class AgentTask:
    """Tarefa para execução pelos agentes"""
    task_id: str
    agent_type: str
    priority: TaskPriority
    payload: Dict[str, Any]
    context: Dict[str, Any]
    created_at: datetime
    deadline: Optional[datetime] = None
    dependencies: List[str] = None

class MiniMaxAgentSystem:
    """Sistema principal de agentes MiniMax M2"""
    
    def __init__(self):
        # Configurar MiniMax M2 API
        self.minimax_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJHdWlsaGVybWUgRHJvbiIsIlVzZXJOYW1lIjoiR3VpbGhlcm1lIERyb24iLCJBY2NvdW50IjoiIiwiU3ViamVjdElEIjoiMTk4NzU4NTc2MTU0ODk2ODA2NCIsIlBob25lIjoiIiwiR3JvdXBJRCI6IjE5ODc1ODU3NjE1NDA1NzU4ODMiLCJQYWdlTmFtZSI6IiIsIk1haWwiOiJkcm9ucmVlZkBnbWFpbC5jb20iLCJDcmVhdGVUaW1lIjoiMjAyNS0xMS0xMCAwMzoyMTozMSIsIlRva2VuVHlwZSI6MSwiaXNzIjoibWluaW1heCJ9.cgcEW8YZEs6DuV2GVZuoIVIytYYjumO5VhaSPA3B4fwS4cQxz32hZS9LaXnTd77QxnlJ548ahGgiMrHi6fYrt61Mx_9Kwi1TdJlXxhG9YFKaf6tAxDOGXw3UyIRKFuHReadV_N5jgoZ-mBXsVXqxCbcsa51NEaXDs2vMiObI8hFEnjJ19mhNG5Jgae2thaWQ0gBQPJ5AQ8D00gdiqJd9yCPzjhJiSOV-KJLSjHjQuQv63x22Lt5f-t-QkPItQlRhLUsV6lXcTM3cJbKHKcoWI5sqbTCEALVKxz9Jup2uK876ldiynt7xKchaAH0ea5XqYPOCM7K6MbCIlNBK-EuMOA"
        
        # Decodificar token para obter informações
        self.decode_token()
        
        # Configurar APIs
        self.minimax_api_url = "https://api.minimax.chat/v1/text/chatcompletion_v2"
        
        # Google Cloud setup
        genai.configure(api_key="AIzaSyC9qLjzZFMkXa5-821NrYu1Y4LPw8wIbfI")
        self.gemini_model = genai.GenerativeModel('gemini-2.5-pro')
        self.bq_client = bigquery.Client()
        
        # Registry de agentes
        self.agents: Dict[str, AgentContext] = {}
        self.active_tasks: Dict[str, AgentTask] = {}
        self.task_queue = asyncio.Queue()
        self.agent_workers = {}
        
        # Sistema de memória compartilhada
        self.shared_memory = {
            "market_data": {},
            "lead_conversations": {},
            "property_matches": {},
            "performance_metrics": {},
            "learning_insights": []
        }
        
        # Sistema de aprendizado
        self.learning_system = {
            "feedback_loop": True,
            "pattern_recognition": True,
            "continuous_improvement": True,
            "knowledge_base": {}
        }
        
        logger.info("🚀 MiniMax Agent System inicializado")
    
    def decode_token(self):
        """Decodifica e exibe informações do token MiniMax"""
        try:
            decoded = jwt.decode(
                self.minimax_token, 
                options={"verify_signature": False}
            )
            
            print("🔐 MiniMax M2 Token Decodificado:")
            print(f"👤 Usuário: {decoded.get('Username', 'N/A')}")
            print(f"🏢 Grupo: {decoded.get('GroupName', 'N/A')}")
            print(f"🆔 Subject ID: {decoded.get('SubjectId', 'N/A')}")
            print(f"📧 Email: {decoded.get('Email', 'N/A')}")
            print(f"🕐 Criado: {decoded.get('CreateTime', 'N/A')}")
            
            return decoded
            
        except Exception as e:
            logger.error(f"Erro ao decodificar token: {e}")
            return None
    
    async def initialize_agents(self):
        """Inicializa todos os agentes especializados"""
        
        # Lead Capture Agent - Responsável por capturar e qualificar leads
        lead_agent = AgentContext(
            agent_id="lead_capture_001",
            name="LeadCaptureMax",
            role="Lead Specialist",
            capabilities=[
                "lead_qualification",
                "conversation_analysis", 
                "intent_detection",
                "personalization",
                "follow_up_automation"
            ],
            memory={},
            learning_patterns=[],
            performance_metrics={"accuracy": 0.0, "conversion_rate": 0.0},
            status=AgentStatus.IDLE,
            last_activity=datetime.now(),
            config={
                "qualification_model": "gemini-2.5-pro",
                "confidence_threshold": 0.75,
                "auto_follow_up": True,
                "response_time_limit": 300  # 5 minutos
            }
        )
        
        # Sales Agent - Responsável por conduzir vendas
        sales_agent = AgentContext(
            agent_id="sales_master_001", 
            name="SalesMax",
            role="Sales Conductor",
            capabilities=[
                "lead_nurturing",
                "objection_handling",
                "proposal_generation",
                "negotiation_support",
                "closing_assistance"
            ],
            memory={},
            learning_patterns=[],
            performance_metrics={"close_rate": 0.0, "avg_deal_size": 0.0},
            status=AgentStatus.IDLE,
            last_activity=datetime.now(),
            config={
                "closing_model": "gemini-2.5-pro",
                "proposal_templates": True,
                "negotiation_strategy": "collaborative"
            }
        )
        
        # Property Matching Agent - Responsável por encontrar propriedades ideais
        property_agent = AgentContext(
            agent_id="property_match_001",
            name="PropertyMatchMax", 
            role="Property Curator",
            capabilities=[
                "property_analysis",
                "market_comparison",
                "preference_matching",
                "recommendation_engine",
                "trend_analysis"
            ],
            memory={},
            learning_patterns=[],
            performance_metrics={"match_accuracy": 0.0, "satisfaction_score": 0.0},
            status=AgentStatus.IDLE,
            last_activity=datetime.now(),
            config={
                "matching_algorithm": "ai_powered",
                "preference_learning": True,
                "market_analysis_depth": "comprehensive"
            }
        )
        
        # Analytics Agent - Responsável por métricas e insights
        analytics_agent = AgentContext(
            agent_id="analytics_max_001",
            name="AnalyticsMax",
            role="Data Scientist", 
            capabilities=[
                "performance_tracking",
                "predictive_analytics",
                "market_insights",
                "conversion_optimization",
                "reporting"
            ],
            memory={},
            learning_patterns=[],
            performance_metrics={"prediction_accuracy": 0.0, "insight_quality": 0.0},
            status=AgentStatus.IDLE,
            last_activity=datetime.now(),
            config={
                "analysis_depth": "deep",
                "prediction_horizon": 90,  # dias
                "real_time_processing": True
            }
        )
        
        # Registrar agentes
        self.agents[lead_agent.agent_id] = lead_agent
        self.agents[sales_agent.agent_id] = sales_agent
        self.agents[property_agent.agent_id] = property_agent
        self.agents[analytics_agent.agent_id] = analytics_agent
        
        print(f"✅ {len(self.agents)} agentes especializados inicializados")
        
        # Inicializar workers para cada agente
        for agent_id in self.agents:
            self.agent_workers[agent_id] = asyncio.create_task(
                self._agent_worker(agent_id)
            )
    
    async def _agent_worker(self, agent_id: str):
        """Worker principal para cada agente"""
        
        while True:
            try:
                agent = self.agents[agent_id]
                
                # Verificar se há tarefas na fila
                try:
                    task = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)
                    
                    if task.agent_type.lower() in agent.role.lower() or agent.agent_id == task.agent_type:
                        await self._execute_agent_task(agent, task)
                    
                    else:
                        # Retornar tarefa para fila se não for para este agente
                        await self.task_queue.put(task)
                
                except asyncio.TimeoutError:
                    # Verificar status e atividades de aprendizado
                    await self._agent_maintenance(agent)
                    await asyncio.sleep(1)
                    
            except Exception as e:
                logger.error(f"Erro no worker do agente {agent_id}: {e}")
                await asyncio.sleep(5)
    
    async def _execute_agent_task(self, agent: AgentContext, task: AgentTask):
        """Executa uma tarefa específica do agente"""
        
        agent.status = AgentStatus.PROCESSING
        agent.last_activity = datetime.now()
        
        try:
            if "lead_capture" in agent.role.lower():
                result = await self._lead_capture_task(agent, task)
            elif "sales" in agent.role.lower():
                result = await self._sales_task(agent, task)
            elif "property" in agent.role.lower():
                result = await self._property_matching_task(agent, task)
            elif "analytics" in agent.role.lower():
                result = await self._analytics_task(agent, task)
            else:
                result = {"error": f"Tipo de tarefa não reconhecida para {agent.name}"}
            
            # Atualizar memória do agente
            await self._update_agent_memory(agent, task, result)
            
            # Registrar métricas de performance
            await self._update_performance_metrics(agent, task, result)
            
            agent.status = AgentStatus.IDLE
            return result
            
        except Exception as e:
            agent.status = AgentStatus.ERROR
            logger.error(f"Erro na execução da tarefa {task.task_id}: {e}")
            return {"error": str(e)}
    
    async def _lead_capture_task(self, agent: AgentContext, task: AgentTask):
        """Tarefa especializada para captura e qualificação de leads"""
        
        lead_data = task.payload
        print(f"📨 {agent.name} processando lead: {lead_data.get('name', 'N/A')}")
        
        # Usar Gemini para qualificação avançada
        qualification_prompt = f"""
        Você é {agent.name}, especialista em leads imobiliários de Natal RN e Parnamirim RN.
        
        Analise este lead usando suas capacidades avançadas:
        
        Lead: {json.dumps(lead_data, ensure_ascii=False, indent=2)}
        
        Contexto do mercado:
        - Crescimento de 88% no mercado imobiliário RN
        - Apartamentos 3 quartos: R$ 300k-500k (Natal), R$ 200k-400k (Parnamirim)
        - Principais zonas: Zona Sul, Ponta Negra, Capim Macio (Natal) / Centro, Eldorado (Parnamirim)
        
        Forneça análise completa incluindo:
        1. Score de qualificação (0-100)
        2. Perfil detalhado do cliente
        3. Estratégia de abordagem recomendada
        4. Próximos passos específicos
        5. Predição de probabilidade de compra
        6. Orçamento estimado
        7. Temporalidade ideal para contato
        8. Preferências de comunicação
        9. Sinais de urgência ou hesitação
        10. Pontos de objection likely
        
        Responda em JSON estruturado.
        """
        
        response = await self.gemini_model.generate_content_async(qualification_prompt)
        qualification = json.loads(response.text)
        
        # Salvar no BigQuery com contexto completo
        await self._save_qualified_lead_to_bigquery(lead_data, qualification, agent)
        
        # Atualizar memória compartilhada
        self.shared_memory["lead_conversations"][lead_data.get('email', '')] = {
            "lead_data": lead_data,
            "qualification": qualification,
            "agent": agent.name,
            "timestamp": datetime.now().isoformat(),
            "next_action": "schedule_follow_up"
        }
        
        # Agendar follow-up automático se necessário
        if qualification.get('score', 0) > 70:
            await self._schedule_automatic_follow_up(lead_data, qualification, agent)
        
        return {
            "status": "success",
            "qualification": qualification,
            "next_steps": qualification.get('next_steps', []),
            "agent_insights": qualification.get('insights', {})
        }
    
    async def _sales_task(self, agent: AgentContext, task: AgentTask):
        """Tarefa especializada para condução de vendas"""
        
        sales_data = task.payload
        print(f"🎯 {agent.name} conduzindo venda: {sales_data.get('lead_name', 'N/A')}")
        
        # Prompt para estratégia de vendas personalizada
        sales_prompt = f"""
        Você é {agent.name}, especialista em vendas imobiliárias de alta performance.
        
        Dados da venda:
        {json.dumps(sales_data, ensure_ascii=False, indent=2)}
        
        Desenvolva estratégia de vendas incluindo:
        
        1. Análise do perfil do cliente
        2. Objections likely e como vencê-las
        3. Benefícios específicos a destacar
        4. Ponto de fechamento ideal
        5. Scripts de follow-up personalizados
        6. Timeline de ações
        7. Incentive structures
        8. Risk mitigation
        9. Competitive advantages
        10. Closing techniques
        
        Foque em aumentar taxa de conversão e valor do deal.
        
        Responda em JSON estruturado.
        """
        
        strategy = await self.gemini_model.generate_content_async(sales_prompt)
        sales_strategy = json.loads(strategy.text)
        
        # Atualizar métricas de vendas
        await self._update_sales_metrics(sales_data, sales_strategy, agent)
        
        return {
            "status": "success",
            "sales_strategy": sales_strategy,
            "action_items": sales_strategy.get('action_items', []),
            "timeline": sales_strategy.get('timeline', []),
            "success_probability": sales_strategy.get('success_probability', 0.0)
        }
    
    async def _property_matching_task(self, agent: AgentContext, task: AgentTask):
        """Tarefa especializada para matching de propriedades"""
        
        client_data = task.payload
        print(f"🏠 {agent.name} buscando propriedades para: {client_data.get('name', 'N/A')}")
        
        # Prompt para busca inteligente de propriedades
        matching_prompt = f"""
        Você é {agent.name}, especialista em matching de propriedades ideiais.
        
        Perfil do cliente:
        {json.dumps(client_data, ensure_ascii=False, indent=2)}
        
        Contexto do mercado imobiliário RN:
        - Natal: Zona Sul (R$ 4k-8k/m²), Ponta Negra (R$ 5k-12k/m²), Capim Macio (R$ 3k-6k/m²)
        - Parnamirim: Centro (R$ 2.5k-4k/m²), Eldorado (R$ 3k-5k/m²)
        - Tendências: crescimento 88% em lançamentos, valorização 7.6% anual
        
        Identifique 3-5 propriedades ideais considerando:
        1. Match com perfil do cliente
        2. Potencial de valorização
        3. Localização estratégica
        4. Relação custo-benefício
        5. Timing de mercado
        6. Comparação com similares
        7. Pros e contras de cada opção
        8. Score de adequação (0-100)
        9. Recommendations finais
        10. Próximos passos
        
        Priorize qualidade sobre quantidade.
        
        Responda em JSON estruturado.
        """
        
        recommendations = await self.gemini_model.generate_content_async(matching_prompt)
        property_matches = json.loads(recommendations.text)
        
        # Atualizar memória de matching
        self.shared_memory["property_matches"][client_data.get('email', '')] = {
            "client_data": client_data,
            "matches": property_matches,
            "agent": agent.name,
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "status": "success",
            "property_matches": property_matches,
            "recommendation_score": property_matches.get('overall_score', 0.0),
            "next_steps": property_matches.get('next_steps', [])
        }
    
    async def _analytics_task(self, agent: AgentContext, task: AgentTask):
        """Tarefa especializada para analytics e insights"""
        
        analytics_data = task.payload
        print(f"📊 {agent.name} processando analytics: {analytics_data.get('type', 'N/A')}")
        
        # Prompt para análise avançada
        analytics_prompt = f"""
        Você é {agent.name}, data scientist especialista em PropTech e mercado imobiliário.
        
        Dados para análise:
        {json.dumps(analytics_data, ensure_ascii=False, indent=2)}
        
        Contexto do sistema:
        - Sistema multi-agente NatPropTech operando
        - Mercado RN: crescimento 88%, valorização 7.6%
        - Pipeline: captura → qualificação → matching → venda
        
        Forneça análise profunda incluindo:
        
        1. Performance metrics detalhadas
        2. Trends identification e predictions
        3. Bottlenecks e optimization opportunities
        4. Customer journey insights
        5. Conversion funnel analysis
        6. ROI calculations e projections
        7. Market positioning assessment
        8. Competitive intelligence
        9. Risk assessment
        10. Strategic recommendations
        
        Seja específico, actionable e orientado a resultados.
        
        Responda em JSON estruturado.
        """
        
        insights = await self.gemini_model.generate_content_async(analytics_prompt)
        analysis_results = json.loads(insights.text)
        
        # Salvar insights na memória compartilhada
        self.shared_memory["learning_insights"].append({
            "timestamp": datetime.now().isoformat(),
            "agent": agent.name,
            "analysis_type": analytics_data.get('type', 'general'),
            "insights": analysis_results,
            "confidence": analysis_results.get('confidence_score', 0.0)
        })
        
        return {
            "status": "success",
            "analysis_results": analysis_results,
            "key_insights": analysis_results.get('key_insights', []),
            "recommendations": analysis_results.get('recommendations', [])
        }
    
    async def _update_agent_memory(self, agent: AgentContext, task: AgentTask, result: Dict):
        """Atualiza a memória do agente com novos aprendizados"""
        
        learning_entry = {
            "timestamp": datetime.now().isoformat(),
            "task_type": task.task_id,
            "input": task.payload,
            "output": result,
            "performance": result.get('success', False),
            "execution_time": (datetime.now() - task.created_at).total_seconds()
        }
        
        agent.memory[f"learning_{len(agent.learning_patterns)}"] = learning_entry
        agent.learning_patterns.append(learning_entry)
        
        # Manter apenas os últimos 100 aprendizados para performance
        if len(agent.learning_patterns) > 100:
            agent.learning_patterns = agent.learning_patterns[-100:]
    
    async def _update_performance_metrics(self, agent: AgentContext, task: AgentTask, result: Dict):
        """Atualiza métricas de performance dos agentes"""
        
        success = result.get('status') == 'success'
        
        if "LeadCapture" in agent.role:
            # Métricas de lead capture
            score = result.get('qualification', {}).get('score', 0)
            agent.performance_metrics["accuracy"] = (agent.performance_metrics["accuracy"] * 0.9) + (score / 100 * 0.1)
            
        elif "Sales" in agent.role:
            # Métricas de vendas
            close_prob = result.get('success_probability', 0)
            current_rate = agent.performance_metrics.get("close_rate", 0.0)
            agent.performance_metrics["close_rate"] = (current_rate * 0.9) + (close_prob * 0.1)
            
        elif "Property" in agent.role:
            # Métricas de matching
            match_score = result.get('recommendation_score', 0)
            current_accuracy = agent.performance_metrics.get("match_accuracy", 0.0)
            agent.performance_metrics["match_accuracy"] = (current_accuracy * 0.9) + (match_score / 100 * 0.1)
            
        elif "Analytics" in agent.role:
            # Métricas de analytics
            confidence = result.get('analysis_results', {}).get('confidence_score', 0)
            current_pred = agent.performance_metrics.get("prediction_accuracy", 0.0)
            agent.performance_metrics["prediction_accuracy"] = (current_pred * 0.9) + (confidence * 0.1)
    
    async def _agent_maintenance(self, agent: AgentContext):
        """Manutenção e aprendizado contínuo dos agentes"""
        
        # Verificar se precisa de aprendizado
        if agent.status == AgentStatus.IDLE:
            agent.status = AgentStatus.LEARNING
            
            # Analisar padrões nos últimos aprendizados
            recent_learning = agent.learning_patterns[-10:] if len(agent.learning_patterns) >= 10 else agent.learning_patterns
            
            if len(recent_learning) >= 5:
                await self._pattern_analysis(agent, recent_learning)
            
            agent.status = AgentStatus.IDLE
    
    async def _pattern_analysis(self, agent: AgentContext, recent_learning: List[Dict]):
        """Análise de padrões para melhoria contínua"""
        
        analysis_prompt = f"""
        Analise os padrões de performance do agente {agent.name}:
        
        Dados recentes:
        {json.dumps(recent_learning, ensure_ascii=False, indent=2)}
        
        Identifique:
        1. Padrões de sucesso/falha
        2. Áreas de melhoria
        3. Otimizações possíveis
        4. Novos aprendizados
        5. Adjustments de estratégia
        
        Foque em melhoria contínua e otimização.
        """
        
        patterns = await self.gemini_model.generate_content_async(analysis_prompt)
        pattern_insights = json.loads(patterns.text)
        
        # Aplicar insights aprendidos
        if "optimizations" in pattern_insights:
            agent.config.update(pattern_insights["optimizations"])
        
        print(f"🧠 {agent.name} Aprendeu: {pattern_insights.get('key_learning', 'Padrões identificados')}")
    
    async def _save_qualified_lead_to_bigquery(self, lead_data: Dict, qualification: Dict, agent: AgentContext):
        """Salva lead qualificado no BigQuery"""
        
        try:
            table_ref = self.bq_client.dataset("natproptech_data").table("qualified_leads")
            table = self.bq_client.get_table(table_ref)
            
            row_to_insert = {
                "timestamp": datetime.now(),
                "agent_id": agent.agent_id,
                "agent_name": agent.name,
                "lead_data": json.dumps(lead_data),
                "qualification": json.dumps(qualification),
                "score": qualification.get('score', 0),
                "qualification_level": qualification.get('qualification', 'cold'),
                "budget_range": qualification.get('budget_range', 'B'),
                "urgency": qualification.get('urgency', 'low'),
                "next_steps": json.dumps(qualification.get('next_steps', [])),
                "confidence": qualification.get('confidence', 0.5),
                "raw_ai_response": json.dumps(qualification)
            }
            
            errors = self.bq_client.insert_rows_json(table, [row_to_insert])
            
            if errors == []:
                print(f"💾 Lead qualificado salvo por {agent.name}")
            else:
                print(f"⚠️ Erro ao salvar lead: {errors}")
                
        except Exception as e:
            print(f"❌ Erro BigQuery: {e}")
    
    async def _schedule_automatic_follow_up(self, lead_data: Dict, qualification: Dict, agent: AgentContext):
        """Agenda follow-up automático para leads qualificados"""
        
        follow_up_task = AgentTask(
            task_id=f"follow_up_{lead_data.get('email', '')}_{int(time.time())}",
            agent_type="sales_master_001",
            priority=TaskPriority.HIGH,
            payload={
                "lead_data": lead_data,
                "qualification": qualification,
                "follow_up_type": "automated_nurturing",
                "strategy": qualification.get('follow_up_strategy', 'personalized_sequence')
            },
            context={"trigger": "high_score_lead", "agent": agent.name},
            created_at=datetime.now()
        )
        
        await self.task_queue.put(follow_up_task)
        print(f"🔄 Follow-up agendado para {lead_data.get('name', 'N/A')}")
    
    async def submit_task(self, task_type: str, payload: Dict, priority: TaskPriority = TaskPriority.MEDIUM) -> str:
        """Submete uma nova tarefa ao sistema"""
        
        task_id = f"{task_type}_{int(time.time())}_{len(self.active_tasks)}"
        
        task = AgentTask(
            task_id=task_id,
            agent_type=task_type,
            priority=priority,
            payload=payload,
            context={},
            created_at=datetime.now()
        )
        
        self.active_tasks[task_id] = task
        await self.task_queue.put(task)
        
        print(f"📋 Tarefa submetida: {task_id}")
        return task_id
    
    async def get_system_status(self) -> Dict:
        """Retorna status completo do sistema"""
        
        return {
            "timestamp": datetime.now().isoformat(),
            "agents": {
                agent_id: {
                    "name": agent.name,
                    "role": agent.role,
                    "status": agent.status.value,
                    "last_activity": agent.last_activity.isoformat(),
                    "performance": agent.performance_metrics,
                    "capabilities": agent.capabilities
                }
                for agent_id, agent in self.agents.items()
            },
            "active_tasks": len(self.active_tasks),
            "queue_size": self.task_queue.qsize(),
            "shared_memory_usage": {
                "lead_conversations": len(self.shared_memory["lead_conversations"]),
                "property_matches": len(self.shared_memory["property_matches"]),
                "learning_insights": len(self.shared_memory["learning_insights"])
            },
            "system_health": "optimal"
        }
    
    async def shutdown(self):
        """Desliga o sistema de forma elegante"""
        
        print("🔄 Desligando sistema de agentes...")
        
        # Cancelar todos os workers
        for task in self.agent_workers.values():
            task.cancel()
        
        # Aguardar finalização
        await asyncio.gather(*self.agent_workers.values(), return_exceptions=True)
        
        print("✅ Sistema de agentes desligado com sucesso")

# 🚀 FUNÇÃO PRINCIPAL PARA TESTE
async def main():
    """Função principal para demonstrar o sistema"""
    
    print("🚀 INICIANDO SISTEMA MINIAGENTES NATPROPTECH")
    print("=" * 60)
    
    # Inicializar sistema
    agent_system = MiniMaxAgentSystem()
    await agent_system.initialize_agents()
    
    # Aguardar inicialização
    await asyncio.sleep(2)
    
    print("\n📋 TESTANDO CAPTURA DE LEADS:")
    # Teste 1: Captura de lead
    lead_task = {
        "name": "Maria Silva Santos",
        "email": "maria.santos@email.com",
        "phone": "(84) 98765-4321",
        "message": "Quero comprar um apartamento de 3 quartos em Natal, próxima ao mar, até R$ 450.000. Pretendo me mudar em 6 meses.",
        "source": "whatsapp",
        "budget_max": 450000,
        "preferred_location": "Natal - Zona Sul",
        "timeline": "6 meses"
    }
    
    await agent_system.submit_task("lead_capture_001", lead_task, TaskPriority.HIGH)
    
    print("\n🎯 TESTANDO ESTRATÉGIA DE VENDAS:")
    # Teste 2: Estratégia de vendas
    sales_task = {
        "lead_name": "Maria Silva Santos",
        "lead_email": "maria.santos@email.com",
        "property_interest": "Apartamento 3 quartos - Natal",
        "budget": 450000,
        "qualification_score": 85,
        "objections": ["preço", "localização", "financiamento"],
        "timeline": "6 meses"
    }
    
    await agent_system.submit_task("sales_master_001", sales_task, TaskPriority.MEDIUM)
    
    print("\n🏠 TESTANDO MATCHING DE PROPRIEDADES:")
    # Teste 3: Matching de propriedades
    property_task = {
        "name": "Maria Silva Santos",
        "email": "maria.santos@email.com", 
        "budget": 450000,
        "bedrooms": 3,
        "location_preference": "Natal - Zona Sul",
        "features": ["vista_mar", "garagem", "varanda"],
        "timeline": "6 meses"
    }
    
    await agent_system.submit_task("property_match_001", property_task, TaskPriority.MEDIUM)
    
    print("\n📊 TESTANDO ANALYTICS:")
    # Teste 4: Analytics
    analytics_task = {
        "type": "performance_analysis",
        "period": "last_7_days",
        "metrics": ["conversion_rate", "lead_quality", "sales_velocity"],
        "focus_area": "optimization"
    }
    
    await agent_system.submit_task("analytics_max_001", analytics_task, TaskPriority.LOW)
    
    # Aguardar processamento
    print("\n⏳ Aguardando processamento dos agentes...")
    await asyncio.sleep(10)
    
    # Verificar status
    print("\n📊 STATUS DO SISTEMA:")
    status = await agent_system.get_system_status()
    print(json.dumps(status, indent=2, ensure_ascii=False))
    
    print("\n✅ DEMONSTRAÇÃO CONCLUÍDA!")
    
    # Manter sistema rodando por um tempo para demonstração
    print("\n🔄 Sistema continuará rodando para demonstração...")
    await asyncio.sleep(30)
    
    # Desligar
    await agent_system.shutdown()

if __name__ == "__main__":
    asyncio.run(main())