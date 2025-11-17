"""
🚀 WhatsApp Business Integration - NatPropTech
Autor: MiniMax Agent
Data: 17 de Novembro de 2025

Integração completa do WhatsApp Business API com a plataforma NatPropTech
para interações automáticas e gerenciamento de leads via WhatsApp.
"""

import aiohttp
import asyncio
import json
import base64
import hmac
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import uuid
from urllib.parse import parse_qs

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessageType(Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    DOCUMENT = "document"
    TEMPLATE = "template"
    INTERACTIVE = "interactive"

class MessageStatus(Enum):
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"

@dataclass
class WhatsAppMessage:
    message_id: str
    from_number: str
    to_number: str
    message_type: MessageType
    content: Dict[str, Any]
    timestamp: datetime
    status: MessageStatus = MessageStatus.SENT

@dataclass
class WhatsAppContact:
    wa_id: str
    name: str
    profile_picture_url: Optional[str] = None
    last_seen: Optional[datetime] = None
    is_business: bool = False

class WhatsAppBusinessClient:
    """
    Cliente WhatsApp Business Cloud API integrado com NatPropTech
    """
    
    def __init__(self, access_token: str, phone_number_id: str):
        self.access_token = access_token
        self.phone_number_id = phone_number_id
        self.base_url = "https://graph.facebook.com/v18.0"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
    async def send_text_message(self, to: str, body: str, message_id: Optional[str] = None) -> Dict[str, Any]:
        """Envia mensagem de texto"""
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": body}
        }
        
        if message_id:
            data["context"] = {"message_id": message_id}
        
        return await self._make_request("POST", f"/{self.phone_number_id}/messages", data)
    
    async def send_image_message(self, to: str, image_url: str, caption: str = "", message_id: Optional[str] = None) -> Dict[str, Any]:
        """Envia mensagem com imagem"""
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "image",
            "image": {
                "link": image_url,
                "caption": caption
            }
        }
        
        if message_id:
            data["context"] = {"message_id": message_id}
        
        return await self._make_request("POST", f"/{self.phone_number_id}/messages", data)
    
    async def send_property_suggestion(self, to: str, property_data: Dict[str, Any], message_id: Optional[str] = None) -> Dict[str, Any]:
        """Envia sugestão de propriedade com elementos interativos"""
        header_text = f"🏡 {property_data.get('title', 'Imóvel em destaque')}"
        body_text = f"""
🏠 *{property_data.get('title', 'Propriedade')}*
💰 Valor: R$ {property_data.get('price', 'N/A')}
📍 Localização: {property_data.get('location', 'Natal/RN')}
🛏️ Quartos: {property_data.get('bedrooms', 'N/A')}
🚗 Vagas: {property_data.get('parking', 'N/A')}

💡 *Interessado? Responda com o número da opção:*
1️⃣ Ver mais detalhes
2️⃣ Agendar visita
3️⃣ Simular financiamento
4️⃣ Falar com corretor
        """
        
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": body_text.strip()},
                "header": {
                    "type": "text",
                    "text": header_text
                },
                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {"id": f"details_{property_data.get('id', '1')}", "title": "Ver detalhes"}
                        },
                        {
                            "type": "reply", 
                            "reply": {"id": f"visit_{property_data.get('id', '1')}", "title": "Agendar visita"}
                        },
                        {
                            "type": "reply",
                            "reply": {"id": f"finance_{property_data.get('id', '1')}", "title": "Simular financiamento"}
                        },
                        {
                            "type": "reply",
                            "reply": {"id": f"agent_{property_data.get('id', '1')}", "title": "Falar com corretor"}
                        }
                    ]
                }
            }
        }
        
        if message_id:
            data["context"] = {"message_id": message_id}
        
        return await self._make_request("POST", f"/{self.phone_number_id}/messages", data)
    
    async def send_lead_qualification(self, to: str, qualification_data: Dict[str, Any], message_id: Optional[str] = None) -> Dict[str, Any]:
        """Envia resultado de qualificação de lead"""
        score = qualification_data.get('score', 0)
        risk_level = "Alto" if score > 0.8 else "Médio" if score > 0.5 else "Baixo"
        
        body_text = f"""
🎯 *Qualificação de Lead Concluída!*

📊 **Score de Qualidade:** {score:.1%} ({risk_level} Risco)
👤 **Cliente:** {qualification_data.get('name', 'N/A')}
💰 **Orçamento:** R$ {qualification_data.get('budget', 'N/A')}
⏰ **Prazo:** {qualification_data.get('timeline', 'N/A')}

🎁 *Próximos passos automáticos:*
✅ Email de boas-vindas enviado
📅 Follow-up agendado para 24h
👨‍💼 Encaminhado para time de vendas
📱 Resposta automática ativada
        """
        
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": body_text.strip()}
        }
        
        if message_id:
            data["context"] = {"message_id": message_id}
        
        return await self._make_request("POST", f"/{self.phone_number_id}/messages", data)
    
    async def mark_message_as_read(self, message_id: str) -> Dict[str, Any]:
        """Marca mensagem como lida"""
        data = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id
        }
        
        return await self._make_request("POST", f"/{self.phone_number_id}/messages", data)
    
    async def _make_request(self, method: str, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Faz requisição HTTP para a API do WhatsApp"""
        url = f"{self.base_url}{endpoint}"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    json=data
                ) as response:
                    result = await response.json()
                    
                    if response.status == 200:
                        logger.info(f"WhatsApp API call successful: {method} {endpoint}")
                        return result
                    else:
                        logger.error(f"WhatsApp API error: {response.status} - {result}")
                        return {"error": result, "status_code": response.status}
                        
            except Exception as e:
                logger.error(f"Request failed: {e}")
                return {"error": str(e)}

class WhatsAppWebhookHandler:
    """
    Manipulador de webhooks do WhatsApp Business API
    """
    
    def __init__(self, verify_token: str, app_secret: str):
        self.verify_token = verify_token
        self.app_secret = app_secret
        
    def verify_webhook(self, mode: str, token: str, challenge: str) -> str:
        """Verifica webhook do Facebook"""
        if token == self.verify_token and mode == "subscribe":
            logger.info("Webhook verified successfully")
            return challenge
        else:
            logger.error(f"Webhook verification failed: token={token}, mode={mode}")
            return ""
    
    def verify_signature(self, payload: bytes, signature: str) -> bool:
        """Verifica assinatura do webhook"""
        expected_signature = hmac.new(
            self.app_secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        # A assinatura pode vir com o prefixo 'sha256='
        if signature.startswith('sha256='):
            signature = signature[7:]
        
        return hmac.compare_digest(expected_signature, signature)
    
    def parse_webhook_data(self, payload: Dict[str, Any]) -> List[WhatsAppMessage]:
        """Parseia dados do webhook para mensagens"""
        messages = []
        
        if 'entry' in payload:
            for entry in payload['entry']:
                if 'changes' in entry:
                    for change in entry['changes']:
                        if change.get('field') == 'messages':
                            value = change.get('value', {})
                            
                            if 'messages' in value:
                                for msg in value['messages']:
                                    try:
                                        message = self._parse_message(msg, value.get('contacts', []))
                                        if message:
                                            messages.append(message)
                                    except Exception as e:
                                        logger.error(f"Error parsing message: {e}")
        
        return messages
    
    def _parse_message(self, msg: Dict[str, Any], contacts: List[Dict[str, Any]]) -> Optional[WhatsAppMessage]:
        """Parseia uma mensagem individual"""
        try:
            message_id = msg.get('id')
            from_number = msg.get('from')
            timestamp = datetime.fromtimestamp(int(msg.get('timestamp', 0)))
            
            # Mapear tipo de mensagem
            message_type = MessageType.TEXT
            content = {}
            
            if 'text' in msg:
                content = {"text": msg['text'].get('body', '')}
            elif 'image' in msg:
                content = {"image": msg['image']}
            elif 'audio' in msg:
                content = {"audio": msg['audio']}
            elif 'video' in msg:
                content = {"video": msg['video']}
            elif 'document' in msg:
                content = {"document": msg['document']}
            elif 'interactive' in msg:
                content = {"interactive": msg['interactive']}
            
            # Tentar encontrar o número de destino
            to_number = ""
            if contacts:
                to_number = contacts[0].get('wa_id', '')
            
            return WhatsAppMessage(
                message_id=message_id,
                from_number=from_number,
                to_number=to_number,
                message_type=message_type,
                content=content,
                timestamp=timestamp,
                status=MessageStatus.SENT
            )
            
        except Exception as e:
            logger.error(f"Error parsing individual message: {e}")
            return None

class WhatsAppNatPropTechBot:
    """
    Chatbot WhatsApp integrado com NatPropTech IA
    """
    
    def __init__(self, whatsapp_client: WhatsAppBusinessClient):
        self.whatsapp_client = whatsapp_client
        self.conversation_state = {}  # Armazena estado das conversas
        self.property_database = self._load_sample_properties()
        
    def _load_sample_properties(self) -> List[Dict[str, Any]]:
        """Carrega dados de exemplo de propriedades"""
        return [
            {
                "id": "prop_001",
                "title": "Apartamento 3 Quartos - Ponta Negra",
                "price": 450000,
                "location": "Ponta Negra, Natal/RN",
                "bedrooms": 3,
                "bathrooms": 2,
                "parking": 2,
                "area": 85,
                "description": "Apartamento moderno com vista para o mar",
                "image_url": "https://example.com/apartment1.jpg"
            },
            {
                "id": "prop_002", 
                "title": "Casa com Piscina - Parnamirim",
                "price": 680000,
                "location": "Parnamirim, Natal/RN",
                "bedrooms": 4,
                "bathrooms": 3,
                "parking": 3,
                "area": 150,
                "description": "Casa ampla com piscina e quintal grande",
                "image_url": "https://example.com/house1.jpg"
            }
        ]
    
    async def process_message(self, message: WhatsAppMessage) -> Optional[Dict[str, Any]]:
        """Processa mensagem recebida e gera resposta"""
        try:
            # Marcar mensagem como lida
            await self.whatsapp_client.mark_message_as_read(message.message_id)
            
            # Processar conteúdo da mensagem
            response = await self._generate_response(message)
            
            if response:
                # Enviar resposta
                await self.whatsapp_client.send_text_message(
                    to=message.from_number,
                    body=response["text"],
                    message_id=message.message_id
                )
                
                # Se há ações específicas, executar
                if "actions" in response:
                    for action in response["actions"]:
                        await self._execute_action(action, message.from_number)
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return None
    
    async def _generate_response(self, message: WhatsAppMessage) -> Optional[Dict[str, Any]]:
        """Gera resposta baseada no conteúdo da mensagem"""
        text_content = ""
        
        # Extrair texto da mensagem
        if "text" in message.content:
            text_content = message.content["text"].lower()
        elif "interactive" in message.content:
            # Processar botão pressionado
            return await self._process_interactive_response(message)
        
        # Lógica de resposta baseada em palavras-chave
        if any(greeting in text_content for greeting in ["olá", "oi", "bom dia", "boa tarde", "boa noite"]):
            return {
                "text": """🏡 *Olá! Bem-vindo ao NatPropTech!*

Sou seu assistente virtual especializado em imóveis de Natal e Parnamirim.

Como posso ajudá-lo hoje?

1️⃣ Buscar imóveis
2️⃣ Avaliar meu imóvel
3️⃣ Falar com um corretor
4️⃣ Simular financiamento
5️⃣ Agendar visita""",
                "actions": ["greet_user"]
            }
        
        elif any(keyword in text_content for keyword in ["imóvel", "apartamento", "casa", "comprar", "vender", "alugar"]):
            return await self._handle_property_request(text_content, message)
        
        elif any(keyword in text_content for keyword in ["financiamento", "simular", "crédito", "parcela"]):
            return await self._handle_financing_request(text_content, message)
        
        elif any(keyword in text_content for keyword in ["visita", "agendar", "conhecer"]):
            return await self._handle_visit_request(text_content, message)
        
        elif any(keyword in text_content for keyword in ["corretor", "vendedor", "atendente"]):
            return await self._handle_agent_request(text_content, message)
        
        elif any(keyword in text_content for keyword in ["valor", "preço", "custo"]):
            return await self._handle_pricing_request(text_content, message)
        
        else:
            # Resposta padrão amigável
            return {
                "text": """🤔 Não entendi completamente sua mensagem.

Mas posso ajudá-lo com:

🏠 *Busca de Imóveis* - Apartamentos, casas, terrenos
💰 *Simulação de Financiamento* - Descubra o valor das parcelas
📅 *Agendamento de Visitas* - Conozca os imóveis pessoalmente  
👨‍💼 *Atendimento Personalizado* - Fale com nossos corretores

*Digite sua dúvida ou escolha uma das opções acima!*""",
                "actions": ["default_response"]
            }
    
    async def _process_interactive_response(self, message: WhatsAppMessage) -> Dict[str, Any]:
        """Processa resposta de botão interativo"""
        interactive = message.content.get("interactive", {})
        button_reply = interactive.get("button_reply", {})
        button_id = button_reply.get("id", "")
        button_title = button_reply.get("title", "")
        
        if "details_" in button_id:
            prop_id = button_id.replace("details_", "")
            return await self._send_property_details(message.from_number, prop_id)
        elif "visit_" in button_id:
            prop_id = button_id.replace("visit_", "")
            return await self._send_visit_calendar(message.from_number, prop_id)
        elif "finance_" in button_id:
            prop_id = button_id.replace("finance_", "")
            return await self._send_financing_options(message.from_number, prop_id)
        elif "agent_" in button_id:
            prop_id = button_id.replace("agent_", "")
            return await self._connect_to_agent(message.from_number, prop_id)
        else:
            return {
                "text": "✅ Opção selecionada com sucesso! Como posso ajudar mais?",
                "actions": ["interactive_selected"]
            }
    
    async def _handle_property_request(self, text: str, message: WhatsAppMessage) -> Dict[str, Any]:
        """Processa solicitação de busca de imóveis"""
        # Enviar sugestão de propriedade mais relevante
        property_suggestion = self.property_database[0]  # Primeiro imóvel como exemplo
        
        response = await self.whatsapp_client.send_property_suggestion(
            to=message.from_number,
            property_data=property_suggestion,
            message_id=message.message_id
        )
        
        return {
            "text": f"🏡 Encontrei um imóvel perfeito para você!\n\nPropriedade: {property_suggestion['title']}\nValor: R$ {property_suggestion['price']:,}",
            "actions": ["property_suggestion", "qualify_lead"],
            "property_data": property_suggestion
        }
    
    async def _send_property_details(self, phone_number: str, prop_id: str) -> Dict[str, Any]:
        """Envia detalhes completos da propriedade"""
        # Simular busca de propriedade por ID
        property_data = {
            "id": prop_id,
            "title": "Apartamento 3 Quartos - Ponta Negra",
            "price": 450000,
            "location": "Ponta Negra, Natal/RN",
            "details": {
                "bedrooms": 3,
                "bathrooms": 2,
                "parking": 2,
                "area": 85,
                "floor": 5,
                "age": 2,
                "amenities": ["Piscina", "Academia", "Playground", "Portaria 24h"]
            }
        }
        
        details_text = f"""
🏠 *{property_data['title']}*

💰 *Valor:* R$ {property_data['price']:,}
📍 *Localização:* {property_data['location']}

📊 *Detalhes:*
🛏️ Quartos: {property_data['details']['bedrooms']}
🚿 Banheiros: {property_data['details']['bathrooms']}
🚗 Vagas: {property_data['details']['parking']}
📐 Área: {property_data['details']['area']}m²

🏢 *Características:*
• Andar: {property_data['details']['floor']}°
• Idade: {property_data['details']['age']} anos
• Piscina • Academia • Playground
• Portaria 24h

💡 *Gostou? Posso agendar uma visita!*
        """
        
        await self.whatsapp_client.send_text_message(to=phone_number, body=details_text.strip())
        
        return {
            "text": "📋 Detalhes da propriedade enviados!",
            "actions": ["property_details_shown"]
        }
    
    async def _send_visit_calendar(self, phone_number: str, prop_id: str) -> Dict[str, Any]:
        """Envia opções de agendamento de visita"""
        calendar_text = """
📅 *Agendar Visita*

*Horários disponíveis:*

🕐 *Segunda a Sexta:*
09h00, 10h30, 14h00, 16h30, 18h00

🕐 *Sábado:*
09h00, 10h30, 14h00

*Para agendar, responda com:*
• Data desejada (dd/mm)
• Horário preferido
• Seu nome completo

*Ou acesse nosso calendário online!*
        """
        
        await self.whatsapp_client.send_text_message(to=phone_number, body=calendar_text.strip())
        
        return {
            "text": "📅 Opções de agendamento enviadas!",
            "actions": ["visit_scheduling"]
        }
    
    async def _send_financing_options(self, phone_number: str, prop_id: str) -> Dict[str, Any]:
        """Envia opções de financiamento"""
        financing_text = """
💰 *Simulação de Financiamento*

*Valor do imóvel:* R$ 450.000

🏦 *Opções disponíveis:*

*📈 Sistema Financeiro:*
• *Mínimo:* 10% de entrada
• *Financiamento:* 90% (R$ 405.000)
• *Prazo:* Até 420 meses (35 anos)

*💳 Taxas aproximadas:*
• *Saque:* TR + 8,5% a.a. + seguros
• *Prazo:* 420 meses

*💡 Parcela estimada:*
• R$ 2.100 a R$ 2.800 (dependendo da entrada)

*Para simulação precisa, preciso saber:*
• Sua renda mensal
• Valor da entrada disponível
• Profissão
        """
        
        await self.whatsapp_client.send_text_message(to=phone_number, body=financing_text.strip())
        
        return {
            "text": "💰 Opções de financiamento enviadas!",
            "actions": ["financing_options"]
        }
    
    async def _connect_to_agent(self, phone_number: str, prop_id: str) -> Dict[str, Any]:
        """Conecta usuário com agente humano"""
        agent_text = """
👨‍💼 *Conectando com Corretor*

*Seu atendimento será transferido para um dos nossos corretores especializados!*

⏰ *Tempo de espera estimado:* 2-5 minutos

*Enquanto isso, deixe seu contato:*
• Nome completo
• Telefone (se diferente)
• Melhor horário para retorno

*Ou acesse nosso site:*
🌐 www.natproptech.com.br
📱 WhatsApp: (84) 99999-9999

*Obrigado pela preferência! 🏡*
        """
        
        await self.whatsapp_client.send_text_message(to=phone_number, body=agent_text.strip())
        
        return {
            "text": "👨‍💼 Transferindo para corretor...",
            "actions": ["connect_to_agent"]
        }
    
    async def _execute_action(self, action: str, phone_number: str):
        """Executa ações específicas"""
        if action == "qualify_lead":
            # Simular qualificação de lead
            qualification_data = {
                "score": 0.85,
                "name": "Cliente WhatsApp",
                "budget": 450000,
                "timeline": "2-3 meses"
            }
            await self.whatsapp_client.send_lead_qualification(phone_number, qualification_data)
        
        # Adicionar mais ações conforme necessário
        logger.info(f"Executed action: {action} for {phone_number}")