"""
🎮 Demo Script - NatPropTech WhatsApp Business Integration
Autor: MiniMax Agent
Data: 17 de Novembro de 2025

Script de demonstração das funcionalidades integradas:
- WhatsApp Business API
- Chatbot inteligente
- Qualificação de leads
- Sugestões de imóveis
- WebSocket em tempo real
"""

import asyncio
import aiohttp
import json
import sys
import os
sys.path.append('/workspace')

from dotenv import load_dotenv
load_dotenv()

class WhatsAppBusinessDemo:
    """Demonstração interativa do WhatsApp Business"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def check_system_health(self):
        """Verifica saúde do sistema"""
        print("🔍 Verificando status do sistema...")
        
        try:
            async with self.session.get(f"{self.base_url}/") as response:
                if response.status == 200:
                    data = await response.json()
                    
                    print("✅ Sistema Online!")
                    print(f"   Status: {data['status']}")
                    print(f"   Versão: {data['version']}")
                    print(f"   Timestamp: {data['timestamp']}")
                    
                    # Verificar sistemas
                    print("\n🤖 Status dos Sistemas:")
                    for system, status in data['systems'].items():
                        status_icon = "✅" if status else "❌"
                        print(f"   {status_icon} {system.replace('_', ' ').title()}")
                    
                    # Verificar WhatsApp
                    print("\n📱 Status WhatsApp:")
                    for feature, status in data['whatsapp'].items():
                        status_icon = "✅" if status else "❌"
                        print(f"   {status_icon} {feature.replace('_', ' ').title()}")
                    
                    return data
                else:
                    print(f"❌ Erro: Status {response.status}")
                    return None
                    
        except Exception as e:
            print(f"❌ Erro de conexão: {e}")
            return None
    
    async def test_whatsapp_messaging(self, phone_number="5584999999999"):
        """Testa envio de mensagem via WhatsApp"""
        print(f"\n💬 Testando envio de mensagem para {phone_number}...")
        
        try:
            message_data = {
                "to": phone_number,
                "message_type": "text",
                "content": {
                    "text": "🏡 *Teste NatPropTech WhatsApp Business*\n\nOlá! Este é um teste da integração com o sistema de IA especializado em imóveis.\n\nComo posso ajudá-lo?\n\n1️⃣ Buscar apartamentos\n2️⃣ Simular financiamento\n3️⃣ Agendar visita"
                }
            }
            
            async with self.session.post(
                f"{self.base_url}/api/whatsapp/send",
                json=message_data
            ) as response:
                result = await response.json()
                
                if result.get('success'):
                    print("✅ Mensagem enviada com sucesso!")
                    print(f"   Result: {result.get('result', {}).get('messages', [{}])[0].get('id', 'N/A')}")
                else:
                    print(f"❌ Erro ao enviar mensagem: {result}")
                    
                return result
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
            return None
    
    async def test_property_suggestion(self, phone_number="5584999999999"):
        """Testa sugestão de propriedade"""
        print(f"\n🏠 Testando sugestão de propriedade para {phone_number}...")
        
        try:
            conversation_data = {
                "phone_number": phone_number,
                "action": "send_property_suggestion",
                "data": {
                    "property_id": "demo_001"
                }
            }
            
            async with self.session.post(
                f"{self.base_url}/api/whatsapp/conversation",
                json=conversation_data
            ) as response:
                result = await response.json()
                
                if result.get('success'):
                    print("✅ Sugestão de propriedade enviada!")
                    print(f"   Ação: {result.get('action')}")
                else:
                    print(f"❌ Erro ao enviar sugestão: {result}")
                    
                return result
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
            return None
    
    async def test_lead_qualification(self, phone_number="5584999999999"):
        """Testa qualificação de lead"""
        print(f"\n🎯 Testando qualificação de lead para {phone_number}...")
        
        try:
            conversation_data = {
                "phone_number": phone_number,
                "action": "qualify_lead"
            }
            
            async with self.session.post(
                f"{self.base_url}/api/whatsapp/conversation",
                json=conversation_data
            ) as response:
                result = await response.json()
                
                if result.get('success'):
                    print("✅ Qualificação de lead enviada!")
                    print(f"   Ação: {result.get('action')}")
                else:
                    print(f"❌ Erro ao qualificar lead: {result}")
                    
                return result
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
            return None
    
    async def get_conversations(self):
        """Busca histórico de conversas"""
        print("\n📊 Verificando conversas...")
        
        try:
            async with self.session.get(f"{self.base_url}/api/whatsapp/conversations") as response:
                if response.status == 200:
                    data = await response.json()
                    
                    print(f"✅ Total de conversas: {data.get('total', 0)}")
                    print(f"   Última atualização: {data.get('last_updated', 'N/A')}")
                    
                    # Mostrar resumo das conversas
                    conversations = data.get('conversations', {})
                    if conversations:
                        print("\n📱 Conversas ativas:")
                        for phone, messages in conversations.items():
                            print(f"   📞 {phone}: {len(messages)} mensagens")
                    else:
                        print("   Nenhuma conversa ativa ainda.")
                    
                    return data
                else:
                    print(f"❌ Erro ao buscar conversas: {response.status}")
                    return None
                    
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
            return None
    
    async def test_websocket_communication(self):
        """Testa comunicação WebSocket"""
        print("\n🔌 Testando comunicação WebSocket...")
        
        try:
            import websockets
            
            async with websockets.connect(f"ws://{self.base_url.replace('http://', '')}/ws") as websocket:
                # Teste 1: Status do WhatsApp
                await websocket.send(json.dumps({"type": "whatsapp_status"}))
                response = await websocket.recv()
                data = json.loads(response)
                print("✅ WebSocket status:", data.get('data', {}))
                
                # Teste 2: Obter conversas
                await websocket.send(json.dumps({"type": "get_conversations"}))
                response = await websocket.recv()
                data = json.loads(response)
                print("✅ WebSocket conversas:", data.get('data', {}))
                
                # Teste 3: Mensagem personalizada
                await websocket.send(json.dumps({
                    "type": "send_test_message",
                    "to": "5584999999999",
                    "message": "Teste WebSocket NatPropTech"
                }))
                response = await websocket.recv()
                data = json.loads(response)
                print("✅ WebSocket mensagem:", data.get('data', {}))
                
        except Exception as e:
            print(f"❌ Erro WebSocket: {e}")
            return None
    
    async def simulate_customer_journey(self):
        """Simula jornada completa do cliente"""
        print("\n🎭 Simulando jornada completa do cliente...")
        print("=" * 60)
        
        # Cliente fictício
        customer_phone = "5584888888888"
        
        steps = [
            ("1. Cliente envia mensagem inicial", lambda: self.send_greeting_message(customer_phone)),
            ("2. Sistema sugere propriedade", lambda: self.test_property_suggestion(customer_phone)),
            ("3. Cliente solicita detalhes", lambda: self.simulate_detailed_request(customer_phone)),
            ("4. Sistema qualifica lead", lambda: self.test_lead_qualification(customer_phone)),
            ("5. Agendamento de visita", lambda: self.simulate_visit_scheduling(customer_phone)),
            ("6. Status final da conversa", lambda: self.check_final_status(customer_phone))
        ]
        
        for step_name, step_function in steps:
            print(f"\n{step_name}")
            print("-" * 40)
            await step_function()
            await asyncio.sleep(1)  # Pausa para simular tempo real
    
    async def send_greeting_message(self, phone_number):
        """Envia mensagem de saudação"""
        message_data = {
            "to": phone_number,
            "message_type": "text",
            "content": {
                "text": "🏡 Olá! Bem-vindo ao NatPropTech! 👋\n\nSou seu assistente virtual especializado em imóveis de Natal e Parnamirim.\n\nComo posso ajudá-lo hoje?\n\n1️⃣ Buscar imóveis\n2️⃣ Avaliar meu imóvel\n3️⃣ Falar com um corretor\n4️⃣ Simular financiamento\n5️⃣ Agendar visita"
            }
        }
        
        try:
            async with self.session.post(
                f"{self.base_url}/api/whatsapp/send",
                json=message_data
            ) as response:
                result = await response.json()
                if result.get('success'):
                    print("   ✅ Saudação enviada com sucesso!")
                else:
                    print(f"   ❌ Erro: {result}")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    async def simulate_detailed_request(self, phone_number):
        """Simula solicitação de detalhes"""
        message_data = {
            "to": phone_number,
            "message_type": "text",
            "content": {
                "text": "Detalhes, por favor! Gostaria de saber mais sobre este apartamento."
            }
        }
        
        try:
            async with self.session.post(
                f"{self.base_url}/api/whatsapp/send",
                json=message_data
            ) as response:
                result = await response.json()
                if result.get('success'):
                    print("   ✅ Detalhes enviados!")
                else:
                    print(f"   ❌ Erro: {result}")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    async def simulate_visit_scheduling(self, phone_number):
        """Simula agendamento de visita"""
        message_data = {
            "to": phone_number,
            "message_type": "text",
            "content": {
                "text": "📅 Agendar visita\n\nPara agendar uma visita, responda com:\n• Data desejada (dd/mm)\n• Horário preferido\n• Seu nome completo\n\nEstamos ansiosos para conhecê-lo!"
            }
        }
        
        try:
            async with self.session.post(
                f"{self.base_url}/api/whatsapp/send",
                json=message_data
            ) as response:
                result = await response.json()
                if result.get('success'):
                    print("   ✅ Agendamento enviado!")
                else:
                    print(f"   ❌ Erro: {result}")
        except Exception as e:
            print(f"   ❌ Erro: {e}")
    
    async def check_final_status(self, phone_number):
        """Verifica status final da conversa"""
        try:
            async with self.session.get(
                f"{self.base_url}/api/whatsapp/conversations/{phone_number}"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"   📊 Mensagens na conversa: {data.get('message_count', 0)}")
                    print(f"   🕐 Última atividade: {data.get('last_activity', 'N/A')}")
                else:
                    print(f"   ❌ Erro ao buscar conversa: {response.status}")
        except Exception as e:
            print(f"   ❌ Erro: {e}")

async def run_comprehensive_demo():
    """Executa demonstração completa"""
    print("🚀 NATPROPTECH WHATSAPP BUSINESS - DEMONSTRAÇÃO COMPLETA")
    print("=" * 80)
    
    # Verificar se servidor está rodando
    base_url = "http://localhost:8000"
    
    async with WhatsAppBusinessDemo(base_url) as demo:
        # 1. Verificação inicial
        health = await demo.check_system_health()
        if not health:
            print("\n❌ Sistema não disponível. Certifique-se de que o servidor está rodando.")
            print(f"   Execute: cd /workspace && python app_whatsapp_integrated.py")
            return
        
        print(f"\n🎯 Sistema disponível! Versão: {health['version']}")
        
        # 2. Menu de demonstração
        while True:
            print("\n" + "=" * 80)
            print("📋 ESCOLHA UMA DEMONSTRAÇÃO:")
            print("1️⃣  Verificar saúde do sistema")
            print("2️⃣  Testar envio de mensagem")
            print("3️⃣  Testar sugestão de propriedade")
            print("4️⃣  Testar qualificação de lead")
            print("5️⃣  Ver conversas ativas")
            print("6️⃣  Testar WebSocket")
            print("7️⃣  Simular jornada completa do cliente")
            print("8️⃣  Demonstração interativa")
            print("0️⃣  Sair")
            print("=" * 80)
            
            choice = input("\n👉 Digite sua opção (0-8): ").strip()
            
            if choice == "0":
                print("\n👋 Obrigado por testar o NatPropTech WhatsApp Business!")
                break
            elif choice == "1":
                await demo.check_system_health()
            elif choice == "2":
                phone = input("📱 Número do telefone (com código do país): ") or "5584999999999"
                await demo.test_whatsapp_messaging(phone)
            elif choice == "3":
                phone = input("📱 Número do telefone: ") or "5584999999999"
                await demo.test_property_suggestion(phone)
            elif choice == "4":
                phone = input("📱 Número do telefone: ") or "5584999999999"
                await demo.test_lead_qualification(phone)
            elif choice == "5":
                await demo.get_conversations()
            elif choice == "6":
                await demo.test_websocket_communication()
            elif choice == "7":
                await demo.simulate_customer_journey()
            elif choice == "8":
                await run_interactive_demo(demo)
            else:
                print("❌ Opção inválida!")
            
            input("\n⏸️ Pressione Enter para continuar...")

async def run_interactive_demo(demo):
    """Executa demonstração interativa completa"""
    print("\n🎭 DEMONSTRAÇÃO INTERATIVA COMPLETA")
    print("=" * 80)
    
    phone = "5584777777777"
    print(f"📱 Usando telefone de teste: {phone}")
    
    demonstrations = [
        ("Verificação do Sistema", demo.check_system_health),
        ("Envio de Mensagem Inicial", lambda: demo.send_greeting_message(phone)),
        ("Sugestão de Propriedade", lambda: demo.test_property_suggestion(phone)),
        ("Qualificação de Lead", lambda: demo.test_lead_qualification(phone)),
        ("Verificação de Conversas", demo.get_conversations),
        ("Teste WebSocket", demo.test_websocket_communication)
    ]
    
    for name, func in demonstrations:
        print(f"\n🔄 {name}...")
        await func()
        await asyncio.sleep(2)
    
    print("\n🎉 Demonstração interativa concluída!")
    print("💡 Acesse o dashboard em: http://localhost:8000/dashboard")

if __name__ == "__main__":
    print("🌟 Iniciando demonstração do NatPropTech WhatsApp Business...")
    print("💡 Certifique-se de que o servidor está rodando primeiro!")
    print("📋 Execute: cd /workspace && python app_whatsapp_integrated.py")
    print()
    
    try:
        asyncio.run(run_comprehensive_demo())
    except KeyboardInterrupt:
        print("\n\n👋 Demonstração interrompida pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro na demonstração: {e}")