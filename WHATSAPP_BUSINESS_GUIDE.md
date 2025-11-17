# 📱 WhatsApp Business Integration - NatPropTech

## 🎯 Visão Geral

Esta documentação detalha a integração completa do **WhatsApp Business API** com a plataforma **NatPropTech MiniMax M2**, permitindo interações inteligentes entre clientes e o sistema de IA especializado em imóveis via WhatsApp.

### ✨ Funcionalidades Principais

- 🤖 **Chatbot Inteligente**: Atendimento automatizado 24/7
- 🏠 **Sugestões de Imóveis**: Recomendações baseadas em preferências
- 📅 **Agendamento Automático**: Sistema de marcação de visitas
- 💰 **Simulação de Financiamento**: Cálculos automáticos de parcelas
- 🎯 **Qualificação de Leads**: Análise automática de potencial
- 👨‍💼 **Transferência para Agentes**: Escalonamento para humanos
- 📊 **Analytics em Tempo Real**: Métricas de conversas e engajamento

---

## 🔧 Configuração Passo a Passo

### 1. Criar App no Meta for Developers

1. Acesse [Meta for Developers](https://developers.facebook.com/)
2. Crie um novo app ou use um existente
3. Selecione **"Business"** como tipo de app
4. Adicione o produto **"WhatsApp Business API"**

### 2. Configurar WhatsApp Business

#### 2.1 Obter Credenciais da API

No painel do seu app, vá em:
```
WhatsApp > API Setup
```

Você encontrará:
- **Access Token** (token de acesso)
- **Phone Number ID** (ID do número)
- **Business Account ID** (ID da conta business)

#### 2.2 Configurar Webhook

1. Configure o webhook com os seguintes parâmetros:
   - **URL de Callback**: `https://seu-dominio.com/webhook/whatsapp`
   - **Token de Verificação**: `natproptech_verify_token`
   - **Campo de Verificação**: `messages`

2. Assine os seguintes eventos:
   - ✅ `messages`
   - ✅ `message_deliveries`
   - ✅ `message_reads`

### 3. Configurar Variáveis de Ambiente

Edite o arquivo `.env` com suas credenciais:

```bash
# WhatsApp Business API Configuration
WHATSAPP_ACCESS_TOKEN=SEU_ACCESS_TOKEN_AQUI
WHATSAPP_PHONE_NUMBER_ID=SEU_PHONE_NUMBER_ID_AQUI
WHATSAPP_VERIFY_TOKEN=natproptech_verify_token
WHATSAPP_APP_SECRET=SEU_APP_SECRET_AQUI
WHATSAPP_BUSINESS_ACCOUNT_ID=SEU_BUSINESS_ACCOUNT_ID_AQUI

# Webhook Configuration
WEBHOOK_URL=https://seu-dominio.com/webhook/whatsapp
WEBHOOK_VERIFY_TOKEN=natproptech_verify_token
```

### 4. Instalar Dependências

```bash
pip install aiohttp pydantic
```

### 5. Executar a Aplicação

```bash
cd /workspace
PYTHONPATH=/workspace /tmp/.venv/bin/python app_whatsapp_integrated.py
```

---

## 🌐 Endpoints da API

### Webhook Endpoints

| Método | URL | Descrição |
|--------|-----|-----------|
| GET | `/webhook/whatsapp/verify` | Verificação do webhook |
| POST | `/webhook/whatsapp` | Recebimento de mensagens |

### API WhatsApp

| Método | URL | Descrição |
|--------|-----|-----------|
| POST | `/api/whatsapp/send` | Enviar mensagem |
| GET | `/api/whatsapp/conversations` | Listar conversas |
| GET | `/api/whatsapp/conversations/{phone}` | Conversa específica |
| POST | `/api/whatsapp/conversation` | Gerenciar conversa |

---

## 💬 Exemplos de Uso

### 1. Enviar Mensagem de Texto

```bash
curl -X POST "http://localhost:8000/api/whatsapp/send" \\
  -H "Content-Type: application/json" \\
  -d '{
    "to": "5584999999999",
    "message_type": "text",
    "content": {
      "text": "🏡 Olá! Como posso ajudá-lo com imóveis?"
    }
  }'
```

### 2. Enviar Sugestão de Imóvel

```bash
curl -X POST "http://localhost:8000/api/whatsapp/conversation" \\
  -H "Content-Type: application/json" \\
  -d '{
    "phone_number": "5584999999999",
    "action": "send_property_suggestion",
    "data": {
      "property_id": "prop_001"
    }
  }'
```

### 3. Qualificar Lead

```bash
curl -X POST "http://localhost:8000/api/whatsapp/conversation" \\
  -H "Content-Type: application/json" \\
  -d '{
    "phone_number": "5584999999999",
    "action": "qualify_lead"
  }'
```

---

## 🤖 Como Funciona o Chatbot

### Fluxo de Conversação

1. **Saudação Inicial**
   ```
   👋 Olá! Bem-vindo ao NatPropTech!
   Como posso ajudá-lo hoje?
   
   1️⃣ Buscar imóveis
   2️⃣ Avaliar meu imóvel
   3️⃣ Falar com um corretor
   4️⃣ Simular financiamento
   5️⃣ Agendar visita
   ```

2. **Busca de Imóveis**
   - Sistema identifica intenção
   - Sugere propriedades relevantes
   - Envia card interativo com opções

3. **Card de Propriedade**
   ```
   🏡 [Título do Imóvel]
   💰 Valor: R$ 450.000
   📍 Localização: Ponta Negra
   🛏️ Quartos: 3 | 🚗 Vagas: 2
   
   [Ver detalhes] [Agendar visita] [Simular financiamento] [Falar com corretor]
   ```

4. **Interações Específicas**
   - **Detalhes**: Envia informações completas
   - **Visita**: Oferece agenda disponível
   - **Financiamento**: Calcula parcelas
   - **Corretor**: Transfere para humano

### Recursos Avançados

- 🧠 **Processamento de Linguagem Natural** (via Gemini AI)
- 📊 **Análise de Sentimento** das mensagens
- 🎯 **Qualificação Automática** de leads
- 🔄 **Aprendizado Contínuo** das interações
- 📱 **Interface Responsiva** para desktop/mobile

---

## 🎨 Interface Web

### Dashboard Principal

Acesse: `http://localhost:8000/dashboard`

**Funcionalidades do Dashboard:**
- 📊 **Métricas em Tempo Real**
- 💬 **Histórico de Conversas**
- 🎯 **Status de Leads**
- 📱 **Configuração WhatsApp**

### WebSocket para Monitoramento

Conecte-se via WebSocket:
```
ws://localhost:8000/ws
```

**Mensagens suportadas:**
```json
{
  "type": "whatsapp_status",
  "data": {}
}

{
  "type": "send_test_message",
  "to": "5584999999999",
  "message": "Teste do sistema"
}

{
  "type": "get_conversations"
}
```

---

## 🔍 Monitoramento e Logs

### Logs da Aplicação

```bash
# Visualizar logs em tempo real
tail -f logs/app.log

# Buscar erros específicos
grep "ERROR" logs/app.log
```

### Métricas Disponíveis

- 📈 **Total de mensagens recebidas**
- 👥 **Conversas ativas**
- 🎯 **Taxa de conversão de leads**
- ⏱️ **Tempo médio de resposta**
- 🏠 **Imóveis mais solicitados**

---

## 🚨 Solução de Problemas

### Webhook não está funcionando?

1. **Verificar URL pública**: Use HTTPS e domínio válido
2. **Testar verificação manual**:
   ```bash
   curl -X GET "https://seu-dominio.com/webhook/whatsapp/verify?hub.mode=subscribe&hub.verify_token=natproptech_verify_token&hub.challenge=test"
   ```
3. **Verificar logs** do servidor

### Erro de assinatura do webhook?

1. **Configurar App Secret**: Certifique-se que está no `.env`
2. **Verificar HTTPS**: Webhook só funciona com HTTPS
3. **Debug da assinatura**:
   ```python
   import hashlib, hmac
   signature = "sha256=signature_aqui"
   expected = hmac.new(app_secret.encode(), payload, hashlib.sha256).hexdigest()
   print(f"Expected: {expected}")
   print(f"Received: {signature[7:]}")
   ```

### Mensagens não chegando?

1. **Verificar credenciais**: Access Token e Phone Number ID
2. **Testar API manualmente**:
   ```bash
   curl -X GET "https://graph.facebook.com/v18.0/{phone_number_id}" \\
     -H "Authorization: Bearer {access_token}"
   ```
3. **Verificar rate limits** da API

### Bot não está respondendo?

1. **Verificar logs** da aplicação
2. **Testar processamento** manual de mensagem
3. **Verificar integração** com Gemini AI

---

## 📋 Checklist de Deploy

### ✅ Antes de Produção

- [ ] Configurar domínio HTTPS válido
- [ ] Obter credenciais WhatsApp Business
- [ ] Testar webhook em ambiente real
- [ ] Configurar monitoramento de logs
- [ ] Implementar autenticação para dashboard
- [ ] Configurar backup de dados
- [ ] Testar todos os fluxos de conversa
- [ ] Validar limites de rate da API

### ✅ Segurança

- [ ] Usar HTTPS obrigatório
- [ ] Validar assinatura de webhooks
- [ ] Sanitizar dados de entrada
- [ ] Implementar rate limiting
- [ ] Configurar CORS adequadamente
- [ ] Armazenar credenciais com segurança

---

## 🎯 Próximos Passos

1. **Personalização Avançada**
   - Treinar modelo específico para imóveis
   - Integrar com CRM existente
   - Adicionar múltiplos idiomas

2. **Funcionalidades Expandidas**
   - Tours virtuais 360°
   - Assinatura digital de contratos
   - Integração com sistemas de pagamento
   - Notificações push para agentes

3. **Analytics Avançados**
   - Dashboard executivo
   - Relatórios automatizados
   - Análise de sentimento
   - Previsões de comportamento

---

## 📞 Suporte

- **Documentação Técnica**: Disponível nos arquivos do projeto
- **Logs de Debug**: `logs/whatsapp_debug.log`
- **Monitoramento**: Dashboard em `http://localhost:8000/dashboard`

---

**🏡 NatPropTech MiniMax M2 + WhatsApp Business**  
*Revolucionando o mercado imobiliário com IA avançada e comunicação inteligente!*