"""
🏡 LEADCAPTURE AGENT - NatPropTech POC
Autor: MiniMax Agent
Data: 17 de Novembro de 2025

Implementação prática do primeiro agente para demonstração.
"""

import google.generativeai as genai
from google.cloud import bigquery
from datetime import datetime
import json
import os
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class LeadQualification:
    """Estrutura para qualificação de lead"""
    score: int
    qualification: str
    budget_range: str
    urgency: str
    preferred_contact: str
    property_type: str
    location_preference: str
    notes: str
    confidence: float

class LeadCaptureAgent:
    """Agente para captura e qualificação de leads usando IA"""
    
    def __init__(self, 
                 project_id: str = "natproptech-rn",
                 gemini_api_key: str = "AIzaSyC9qLjzZFMkXa5-821NrYu1Y4LPw8wIbfI"):
        
        # Configurar Gemini
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        
        # Configurar BigQuery
        self.client = bigquery.Client(project=project_id)
        self.dataset_id = "natproptech_data"
        self.table_id = "leads"
        
        # Contadores para métricas
        self.leads_processed = 0
        self.avg_score = 0.0
        
        print("✅ LeadCapture Agent inicializado com sucesso")
    
    async def capture_lead(self, 
                          name: str, 
                          email: str, 
                          phone: str,
                          message: str = "",
                          source: str = "website",
                          behavior_data: Dict = None) -> Dict:
        """Captura um lead e retorna informações básicas"""
        
        lead_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "message": message,
            "source": source,
            "behavior_data": behavior_data or {},
            "timestamp": datetime.now()
        }
        
        print(f"📨 Lead capturado: {name} ({email})")
        return lead_data
    
    async def qualify_lead_with_ai(self, lead_data: Dict) -> LeadQualification:
        """Qualifica lead usando IA do Gemini"""
        
        # Prompt específico para mercado imobiliário do RN
        prompt = f"""
        Você é um especialista em qualificação de leads para imóveis em Natal RN e Parnamirim RN.
        
        Analise o lead abaixo e forneça qualificação detalhada:
        
        Dados do Lead:
        - Nome: {lead_data.get('name', '')}
        - Email: {lead_data.get('email', '')}
        - Telefone: {lead_data.get('phone', '')}
        - Mensagem: {lead_data.get('message', '')}
        - Fonte: {lead_data.get('source', '')}
        
        Contexto de mercado:
        - Natal RN: apartamentos de 3 quartos entre R$ 300k-500k
        - Parnamirim RN: apartamentos de 2-3 quartos entre R$ 200k-400k
        - Crescimento de 88% no mercado imobiliário regional
        
        Responda APENAS com um JSON válido (sem markdown, sem explicações):
        {{
            "score": <0-100>,
            "qualification": "hot/warm/cold",
            "budget_range": "A (até R$ 300k)/B (R$ 300k-600k)/C (>R$ 600k)",
            "urgency": "high/medium/low",
            "preferred_contact": "whatsapp/email/call",
            "property_type": "apartamento/casa/terreno/comercial",
            "location_preference": "Natal/Parnamirim/zona específica",
            "notes": "<análise detalhada em português>",
            "confidence": <0.0-1.0>
        }}
        """
        
        try:
            print("🤖 Qualificando lead com IA...")
            response = self.model.generate_content(prompt)
            
            # Parse da resposta
            result = json.loads(response.text)
            
            qualification = LeadQualification(
                score=result.get('score', 0),
                qualification=result.get('qualification', 'cold'),
                budget_range=result.get('budget_range', 'B'),
                urgency=result.get('urgency', 'low'),
                preferred_contact=result.get('preferred_contact', 'whatsapp'),
                property_type=result.get('property_type', 'apartamento'),
                location_preference=result.get('location_preference', 'Natal'),
                notes=result.get('notes', ''),
                confidence=result.get('confidence', 0.5)
            )
            
            print(f"✅ Qualificação: {qualification.qualification} (Score: {qualification.score})")
            return qualification
            
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao fazer parse da resposta: {e}")
            return self._fallback_qualification()
        except Exception as e:
            print(f"❌ Erro na qualificação: {e}")
            return self._fallback_qualification()
    
    def _fallback_qualification(self) -> LeadQualification:
        """Qualificação padrão em caso de erro"""
        return LeadQualification(
            score=30,
            qualification="cold",
            budget_range="B",
            urgency="low",
            preferred_contact="whatsapp",
            property_type="apartamento",
            location_preference="Natal",
            notes="Qualificação automática por erro no sistema",
            confidence=0.1
        )
    
    async def save_to_bigquery(self, lead_data: Dict, qualification: LeadQualification) -> bool:
        """Salva lead qualificado no BigQuery"""
        
        try:
            table_ref = self.client.dataset(self.dataset_id).table(self.table_id)
            table = self.client.get_table(table_ref)
            
            row_to_insert = {
                "timestamp": datetime.now(),
                "name": lead_data.get('name', ''),
                "email": lead_data.get('email', ''),
                "phone": lead_data.get('phone', ''),
                "score": qualification.score,
                "qualification": qualification.qualification,
                "budget_range": qualification.budget_range,
                "urgency": qualification.urgency,
                "notes": qualification.notes,
                "source": lead_data.get('source', ''),
                "raw_qualification": json.dumps({
                    "preferred_contact": qualification.preferred_contact,
                    "property_type": qualification.property_type,
                    "location_preference": qualification.location_preference,
                    "confidence": qualification.confidence
                })
            }
            
            errors = self.client.insert_rows_json(table, [row_to_insert])
            
            if errors == []:
                print(f"💾 Lead salvo no BigQuery com sucesso")
                self.leads_processed += 1
                return True
            else:
                print(f"❌ Erro ao salvar no BigQuery: {errors}")
                return False
                
        except Exception as e:
            print(f"❌ Erro na conexão com BigQuery: {e}")
            return False
    
    async def process_lead(self, 
                          name: str,
                          email: str,
                          phone: str,
                          message: str = "",
                          source: str = "website") -> Dict:
        """Processa lead completo: captura, qualifica e salva"""
        
        try:
            # 1. Capturar lead
            lead_data = await self.capture_lead(name, email, phone, message, source)
            
            # 2. Qualificar com IA
            qualification = await self.qualify_lead_with_ai(lead_data)
            
            # 3. Salvar no BigQuery
            saved = await self.save_to_bigquery(lead_data, qualification)
            
            # 4. Retornar resultado
            result = {
                "success": True,
                "lead_id": f"nat-{hash(email)}",
                "lead_data": lead_data,
                "qualification": qualification.__dict__,
                "next_steps": {
                    "contact_method": qualification.preferred_contact,
                    "priority": "high" if qualification.urgency == "high" else "medium",
                    "estimated_budget": qualification.budget_range
                },
                "saved_to_db": saved,
                "processing_time": f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            }
            
            return result
            
        except Exception as e:
            print(f"❌ Erro no processamento: {e}")
            return {
                "success": False,
                "error": str(e),
                "lead_id": f"error-{hash(email)}"
            }
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas do agente"""
        return {
            "leads_processed": self.leads_processed,
            "avg_score": self.avg_score,
            "dataset": self.dataset_id,
            "table": self.table_id,
            "status": "active"
        }

# 🔧 FUNÇÃO PARA TESTE RÁPIDO
async def test_agent():
    """Função para testar o agente com dados de exemplo"""
    
    print("🧪 TESTANDO LEADCAPTURE AGENT")
    print("=" * 50)
    
    # Inicializar agente
    agent = LeadCaptureAgent()
    
    # Teste com lead de exemplo
    test_leads = [
        {
            "name": "Maria Silva",
            "email": "maria@email.com",
            "phone": "(84) 98888-7777",
            "message": "Quero comprar um apartamento de 3 quartos em Natal, orçamento até R$ 450.000",
            "source": "whatsapp"
        },
        {
            "name": "João Santos",
            "email": "joao@empresa.com.br",
            "phone": "(84) 97777-6666",
            "message": "Interessado em apartamento para investimento, até R$ 300.000",
            "source": "website"
        }
    ]
    
    for i, lead in enumerate(test_leads, 1):
        print(f"\n📋 TESTE {i}:")
        result = await agent.process_lead(**lead)
        
        if result["success"]:
            qual = result["qualification"]
            print(f"✅ {lead['name']}: {qual['qualification']} (Score: {qual['score']})")
            print(f"💰 Orçamento: {qual['budget_range']}")
            print(f"📞 Contato: {qual['preferred_contact']}")
        else:
            print(f"❌ Erro: {result.get('error', 'Desconhecido')}")
    
    # Mostrar estatísticas
    print(f"\n📊 ESTATÍSTICAS:")
    print(agent.get_stats())

# 🚀 EXECUÇÃO DIRETA
if __name__ == "__main__":
    import asyncio
    
    # Executar teste
    asyncio.run(test_agent())
    
    print("\n🎯 Para usar em produção:")
    print("agent = LeadCaptureAgent()")
    print("result = await agent.process_lead(")
    print("    name='Nome do Cliente',")
    print("    email='cliente@email.com',")
    print("    phone='(84) 99999-9999',")
    print("    message='Quero comprar apartamento...'")
    print(")")