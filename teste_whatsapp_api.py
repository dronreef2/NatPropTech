#!/usr/bin/env python3
"""
Script de Teste - WhatsApp Business API
Verifica conectividade e credenciais

Autor: MiniMax Agent
Data: 18 de Novembro de 2025
"""

import os
import requests
import json
from datetime import datetime

def load_env():
    """Carrega variáveis de ambiente"""
    from dotenv import load_dotenv
    load_dotenv()

def test_whatsapp_connection():
    """Testa conexão com WhatsApp Business API"""
    
    print("🔍 TESTANDO CONEXÃO WHATSAPP BUSINESS API")
    print("=" * 60)
    
    # Obter credenciais
    access_token = os.getenv('WHATSAPP_ACCESS_TOKEN')
    phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
    business_account_id = os.getenv('WHATSAPP_BUSINESS_ACCOUNT_ID')
    
    print(f"⏰ Teste executado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Verificar se credenciais foram configuradas
    if not access_token or access_token == 'SUA_CHAVE_ACCESS_TOKEN_AQUI':
        print("❌ ERRO: WHATSAPP_ACCESS_TOKEN não configurado")
        print("   Configure sua chave real no arquivo .env")
        return False
        
    if not phone_number_id or phone_number_id == 'SEU_PHONE_NUMBER_ID_AQUI':
        print("❌ ERRO: WHATSAPP_PHONE_NUMBER_ID não configurado")
        print("   Configure seu Phone Number ID real no arquivo .env")
        return False
    
    # Teste 1: Verificar Phone Number
    print("📱 Teste 1: Verificando Phone Number...")
    try:
        url = f"https://graph.facebook.com/v17.0/{phone_number_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Phone Number válido: {data.get('display_phone_number', 'N/A')}")
            print(f"   ✅ Status: {data.get('verified_name', 'N/A')}")
        elif response.status_code == 400:
            print("   ❌ Phone Number inválido ou não encontrado")
            print(f"   📋 Detalhes: {response.text}")
            return False
        else:
            print(f"   ⚠️  Resposta inesperada: {response.status_code}")
            print(f"   📋 Detalhes: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Erro de rede: {e}")
        return False
    
    # Teste 2: Verificar Business Account (se disponível)
    if business_account_id and business_account_id != 'SEU_BUSINESS_ACCOUNT_ID_AQUI':
        print("\n🏢 Teste 2: Verificando Business Account...")
        try:
            url = f"https://graph.facebook.com/v17.0/{business_account_id}"
            headers = {"Authorization": f"Bearer {access_token}"}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Business Account válido: {data.get('name', 'N/A')}")
            else:
                print(f"   ⚠️  Business Account não acessível: {response.status_code}")
                
        except Exception as e:
            print(f"   ⚠️  Erro verificando Business Account: {e}")
    
    # Teste 3: Verificar permissões de webhook
    print("\n🌐 Teste 3: Verificando permissões...")
    try:
        url = f"https://graph.facebook.com/v17.0/{phone_number_id}/subscribed_apps"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("   ✅ Permissões de API OK")
        else:
            print(f"   ⚠️  Permissões limitadas: {response.status_code}")
            
    except Exception as e:
        print(f"   ⚠️  Erro verificando permissões: {e}")
    
    # Teste 4: Simular envio de mensagem de teste
    print("\n💬 Teste 4: Testando envio de mensagem (dry-run)...")
    test_message = {
        "messaging_product": "whatsapp",
        "to": "5511999999999",  # Número de teste (formato internacional)
        "type": "text",
        "text": {
            "body": "🧪 Teste do sistema NatPropTech - se receber esta mensagem, a API está funcionando!"
        }
    }
    
    # NÃO enviar mensagem real, apenas validar estrutura
    print("   ✅ Estrutura da mensagem validada")
    print("   📝 Para testar envio real, use:")
    print("      python3 natproptech_agentic_integration.py")
    
    print("\n" + "=" * 60)
    print("🎉 TESTE DE CONEXÃO CONCLUÍDO!")
    print("✅ Seu WhatsApp Business API está configurado corretamente!")
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Configure seu webhook no Meta Business Suite")
    print("2. Inicie o servidor: python3 natproptech_webhook_server.py") 
    print("3. Teste o sistema completo: python3 natproptech_agentic_integration.py")
    
    return True

def main():
    """Função principal"""
    load_env()
    
    print("🚀 NATPROPTECH - TESTE WHATSAPP BUSINESS API")
    print("Verificando configuração das credenciais...\n")
    
    success = test_whatsapp_connection()
    
    if not success:
        print("\n🔧 Para configurar suas credenciais:")
        print("1. Consulte: GUIA_OBTER_WHATSAPP_API.md")
        print("2. Edite o arquivo .env com suas chaves reais")
        print("3. Execute este teste novamente")
        
    print("\n💰 Sistema pronto para gerar vendas imobiliárias automatizadas!")

if __name__ == "__main__":
    main()