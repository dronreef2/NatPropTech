# 🚀 COMANDOS RÁPIDOS NATPROPTECH

## ⚡ Setup Rápido (Recomendado)
```bash
# 1. Configuração automática completa
python3 setup_natproptech_automatic.py

# 2. Testar sistema
python3 natproptech_agentic_integration.py

# 3. Iniciar servidor webhook
python3 natproptech_webhook_server.py
```

## 🔧 Configuração Manual
```bash
# 1. Criar arquivo .env manualmente
cat > .env << EOF
WHATSAPP_ACCESS_TOKEN=seu_token_permanente
WHATSAPP_PHONE_NUMBER_ID=seu_phone_id
WHATSAPP_BUSINESS_ACCOUNT_ID=seu_business_id
WHATSAPP_VERIFY_TOKEN=natproptech_verify_token
EOF

# 2. Instalar dependências
pip install flask python-dotenv aiohttp openai google-generativeai

# 3. Validar configuração
python3 -c "from natproptech_agentic_integration import validate_environment; validate_environment()"
```

## 🧪 Testes e Validação
```bash
# Teste completo do sistema
python3 natproptech_agentic_integration.py

# Demonstração MiniMax Orchestrator
python3 minimax_natproptech_sales_orchestrator.py

# Health check do webhook
curl http://localhost:5000/health

# Ver estatísticas
curl http://localhost:5000/stats

# Ver configuração
curl http://localhost:5000/config
```

## 🌐 Servidor Webhook
```bash
# Iniciar servidor (porta 5000)
python3 natproptech_webhook_server.py

# Iniciar em background
nohup python3 natproptech_webhook_server.py > webhook.log 2>&1 &

# Parar servidor
pkill -f natproptech_webhook_server.py

# Ver logs
tail -f natproptech_webhook.log
```

## 📱 Webhook WhatsApp Meta Configuration
```
URL: https://seusite.com/webhook
Verify Token: natproptech_verify_token
Subscriptions: messages, message_deliveries, message_reads, message_reactions, message_replies
```

## 🔍 Debug e Troubleshooting
```bash
# Validar credenciais
python3 -c "from natproptech_agentic_integration import validate_environment; validate_environment()"

# Testar conexão WhatsApp API
python3 -c "
import requests
import os
token = os.getenv('WHATSAPP_ACCESS_TOKEN')
phone_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
r = requests.get(f'https://graph.facebook.com/v17.0/{phone_id}', headers={'Authorization': f'Bearer {token}'})
print('Status:', r.status_code)
"

# Verificar logs de erro
tail -f natproptech_webhook.log | grep ERROR

# Testar envio de mensagem
python3 -c "
import asyncio
from natproptech_agentic_integration import WhatsAppBusinessIntegration
from natproptech_agentic_integration import load_environment_config
config = load_environment_config()
whatsapp = WhatsAppBusinessIntegration(config['whatsapp']['access_token'], config['whatsapp']['phone_number_id'])
result = asyncio.run(whatsapp.send_text_message('+5584999999999', 'Teste do sistema!'))
print(result)
"
```

## 💰 Monitoramento de ROI
```bash
# Ver estatísticas do sistema
curl http://localhost:5000/stats | jq

# Processamento de mensagens
tail -f natproptech_webhook.log | grep "processamento concluído"

# Conversões e leads
grep "Score:" natproptech_webhook.log | tail -10
```

## 🛠️ Comandos de Manutenção
```bash
# Backup das configurações
cp .env .env.backup.$(date +%Y%m%d)

# Limpeza de logs antigos
find . -name "*.log" -mtime +7 -delete

# Verificar processos rodando
ps aux | grep python

# Reiniciar serviços
pkill -f natproptech_webhook_server.py
sleep 2
python3 natproptech_webhook_server.py &
```

## 📊 Métricas Importantes
- **Tempo de Resposta**: < 5 segundos
- **Taxa de Conversão**: > 5%
- **Disponibilidade**: > 99%
- **Lead Score Médio**: > 0.7

## 🚨 Alertas Críticos
- Se tempo de resposta > 5 segundos
- Se taxa de conversão < 5%
- Se sistema ficar indisponível
- Se rate limits forem atingidos

---

**💡 Dica**: Use `setup_natproptech_automatic.py` para configuração completa em 5 minutos!