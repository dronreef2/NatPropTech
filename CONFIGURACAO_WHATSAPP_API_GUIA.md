# Guia Completo: Configuração WhatsApp Business API para NatPropTech

**Data:** 17 de Novembro de 2025  
**Sistema:** NatPropTech Agentic Sales Platform  
**Objetivo:** Configurar credenciais reais do WhatsApp Business API

## 📋 Checklist de Configuração

### ✅ Passo 1: Pré-requisitos
- [ ] Conta Meta Business verificada
- [ ] WhatsApp Business Account criada
- [ ] Número de telefone verificado
- [ ] Cartão de crédito cadastrado na Meta

### ✅ Passo 2: Obter Credenciais no Meta Business Suite

#### 2.1 Acessar Meta for Developers
1. Acesse: https://developers.facebook.com/
2. Faça login com sua conta Meta Business
3. Vá para "My Apps" > "Create App"

#### 2.2 Criar Aplicação WhatsApp Business
1. **Tipo de App:** "Business"
2. **Nome:** "NatPropTech Sales Bot"
3. **Email de Contato:** seu-email@empresa.com

#### 2.3 Configurar WhatsApp Business API
1. No menu lateral, vá para "WhatsApp" > "Getting Started"
2. Clique em "Set Up" no Webhooks
3. **IMPORTANTE:** Anote as informações:
   - **Phone Number ID:** (formato: 1234567890123456)
   - **WhatsApp Business Account ID:** (formato: 9876543210987654)
   - **Access Token:** (temporário no início)

#### 2.4 Gerar Access Token Permanente
1. Vá para "WhatsApp" > "API Setup"
2. Clique em "System Users" no menu lateral
3. Crie um System User:
   - Nome: "NatPropTech-SalesBot"
   - Sistema Type: "System user"
4. Gerar Token:
   - Vá para o System User criado
   - Clique em "Generate New Token"
   - **Scopes:** Select all WhatsApp API permissions
   - **Token Expiry:** No expiration (recommended for production)
5. **SALVE ESTE TOKEN** - você não conseguirá vê-lo novamente!

### ✅ Passo 3: Configurar Webhooks

#### 3.1 URL do Webhook
```
https://seusite.com/webhook
```
**Substitua por seu domínio real**

#### 3.2 Verification Token
```
natproptech_verify_token
```
(ou um token de sua escolha)

#### 3.3 Subscriptions (marque todas):
- [x] messages
- [x] message_deliveries
- [x] message_reads
- [x] message_reactions
- [x] message_replies

#### 3.4 Campos de Verificação do Webhook:
```
phone_number_id: Seu Phone Number ID
access_token: Seu Access Token
webhook_verify_token: natproptech_verify_token
```

### ✅ Passo 4: Configurar Variáveis de Ambiente

Crie um arquivo `.env` no diretório do projeto:

```env
# WhatsApp Business API Credentials
WHATSAPP_ACCESS_TOKEN=seu_access_token_permanente
WHATSAPP_PHONE_NUMBER_ID=seu_phone_number_id
WHATSAPP_BUSINESS_ACCOUNT_ID=seu_business_account_id
WHATSAPP_VERIFY_TOKEN=natproptech_verify_token

# Meta Business Configuration
META_BUSINESS_APP_ID=seu_app_id
META_BUSINESS_APP_SECRET=seu_app_secret

# Database (se usando)
DATABASE_URL=sqlite:///natproptech.db

# MiniMax Agent
MINIMAX_AGENT_TOKEN=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
GEMINI_API_KEY=sua_gemini_api_key
```

### ✅ Passo 5: Configuração de Produção

#### 5.1 Domínio e SSL
- Configure um domínio HTTPS válido
- Certificados SSL obrigatórios para webhooks

#### 5.2 Server Requirements
```bash
# Portas necessárias
- 80 (HTTP - redirecionamento)
- 443 (HTTPS - produção)
- 5000-5010 (aplicação)
```

#### 5.3 Firewall
```
Portas TCP a liberar:
- 80, 443 (web)
- 5000-5010 (aplicação)
```

### ✅ Passo 6: Teste de Conectividade

#### 6.1 Teste Webhook
```bash
# Verificar webhook configurado
curl -X GET https://graph.facebook.com/v17.0/YOUR_PHONE_NUMBER_ID/webhooks \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### 6.2 Teste Envio de Mensagem
```python
# Código para testar
import requests

token = "SEU_ACCESS_TOKEN"
phone_number_id = "SEU_PHONE_NUMBER_ID"

url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

data = {
    "messaging_product": "whatsapp",
    "to": "SEU_NUMERO_TESTE",
    "text": {
        "body": "Teste do sistema NatPropTech! 🚀"
    }
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
```

## 🚨 IMPORTANTE: Limites da API

### Rate Limits WhatsApp Business API:
- **Mensagens de texto:** 1000 por segundo
- **Templates:** 400 por minuto
- **Mídia:** 400 por minuto
- **Webhooks:** 5000 eventos por segundo

### Custos Estimados:
- **Primeiras 1.000 conversas:** Grátis
- **Conversas adicionais:** R$ 0.20 por conversa
- **Para 2.847 leads/mês:** ~R$ 370/mês

## 🔒 Segurança e Compliance

### Políticas Obrigatórias:
- [ ] Política de Privacidade atualizada
- [ ] Termos de Uso alinhados com WhatsApp
- [ ] Opt-out claro para usuários
- [ ] Logs de consentimento

### Dados Pessoais:
- Não armazenar mensagens sem consentimento
- Criptografar dados sensíveis
- Implementar LGPD compliance

## 📞 Suporte e Monitoramento

### Logs Importantes:
```python
# Monitorar estes logs
- webhook_receive_time
- message_processing_duration
- agent_confidence_score
- lead_conversion_rate
```

### Alertas Recomendados:
- Falhas no webhook
- Rate limits atingidos
- Tempo de resposta > 5 segundos
- Conversões abaixo de 5%

## 🎯 Próximos Passos Após Configuração

1. **Teste completo** com número controlado
2. **Configurar Respond.io** (se escolher)
3. **Treinar equipe** no sistema
4. **Monitorar métricas** por 1 semana
5. **Otimizar fluxos** baseado nos dados
6. **Escalar campanha** gradualmente

## 📧 Contatos de Emergência

- **Meta Business Support:** business.facebook.com/support
- **WhatsApp Business API:** https://developers.facebook.com/docs/whatsapp
- **Status Dashboard:** https://developers.facebook.com/status

---

**Status Atual:** Aguardando credenciais reais  
**Próxima Ação:** Configurar webhooks no Meta Business Suite  
**Tempo Estimado:** 2-3 horas para configuração completa