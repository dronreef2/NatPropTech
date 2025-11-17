# 🚀 GUIA PASSO-A-PASSO: OBTER CREDENCIAIS WHATSAPP BUSINESS API

## 📋 PRÉ-REQUISITOS
- Conta comercial no Facebook/Instagram
- Site ou domínio com HTTPS
- Número de telefone para verificação

---

## 🎯 ETAPA 1: ACESSAR O META FOR DEVELOPERS

1. **Acesse**: https://developers.facebook.com/
2. **Faça login** com sua conta comercial
3. **Clique** em "Meu Apps" > "Criar App"
4. **Selecione** "Negócio" > "Próximo"
5. **Preencha**:
   - Nome do app: `NatPropTech Vendas`
   - Email de contato: seu@email.com
   - Conta comercial: selecione a sua

---

## 🎯 ETAPA 2: CONFIGURAR WHATSAPP BUSINESS API

1. **No painel do app**, encontre a seção "WhatsApp"
2. **Clique** em "Configurar" ou "Set up"
3. **Siga** o assistente de configuração:
   - Aceite os termos de uso
   - Adicione o número de telefone da empresa
   - Faça a verificação via SMS/chamada

---

## 🎯 ETAPA 3: OBTER AS CREDENCIAIS ESSENCIAIS

Após a configuração, você encontrará estas informações no painel:

### 🔑 3.1 ACCESS TOKEN (Obrigatório)
- **Localização**: seção "API Setup"
- **Formato**: string longa (200+ caracteres)
- **Exemplo**: `EAAG3xCKocmABO9v...

### 🔢 3.2 PHONE NUMBER ID (Obrigatório)  
- **Localização**: seção "Phone Numbers"
- **Formato**: apenas números
- **Exemplo**: `9876543210`

### 🏢 3.3 BUSINESS ACCOUNT ID (Obrigatório)
- **Localização**: seção "Business Account" 
- **Formato**: apenas números
- **Exemplo**: `1234567890`

### 🔐 3.4 APP SECRET (Recomendado)
- **Localização**: Configurações > Básico
- **Formato**: combinação de letras e números
- **Exemplo**: `abc123def456`

---

## 🎯 ETAPA 4: CONFIGURAR WEBHOOK

### 4.1 URL do Webhook
```
https://SEU_DOMINIO.com/webhook
```

### 4.2 Verify Token
```
natproptech_verify_token
```

### 4.3 Assinaturas para Ativar
- ✅ `messages`
- ✅ `message_deliveries` 
- ✅ `message_reads`
- ✅ `message_reactions`
- ✅ `message_replies`

---

## 🎯 ETAPA 5: INSERIR CREDENCIAIS NO SISTEMA

Edite o arquivo `.env` no seu projeto:

```bash
nano .env
```

Substitua os valores placeholder:

```bash
# Suas credenciais reais do WhatsApp
WHATSAPP_ACCESS_TOKEN=EAAG3xCKocm_mBlaBlaBla...
WHATSAPP_PHONE_NUMBER_ID=9876543210
WHATSAPP_BUSINESS_ACCOUNT_ID=1234567890  
WHATSAPP_APP_SECRET=abc123def456

# Verificar se estas estão corretas
WHATSAPP_VERIFY_TOKEN=natproptech_verify_token
WEBHOOK_URL=https://seu-dominio.com/webhook
```

---

## 🎯 ETAPA 6: TESTE DE CONECTIVIDADE

Execute o teste de conexão:

```bash
python3 -c "
import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('WHATSAPP_ACCESS_TOKEN')
phone_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')

if token and phone_id:
    url = f'https://graph.facebook.com/v17.0/{phone_id}'
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            print('✅ Conexão com WhatsApp API bem-sucedida!')
            print('📱 Número verificado e ativo')
        else:
            print(f'❌ Erro: {response.status_code}')
            print(response.text)
    except Exception as e:
        print(f'❌ Erro de conexão: {e}')
else:
    print('❌ Credenciais não configuradas corretamente')
"
```

---

## 🎯 ETAPA 7: INICIAR SISTEMA

Após configurar as credenciais:

1. **Iniciar webhook server**:
```bash
python3 natproptech_webhook_server.py
```

2. **Testar sistema completo**:
```bash
python3 natproptech_agentic_integration.py
```

3. **Monitorar logs**:
```bash
tail -f natproptech_webhook.log
```

---

## 💰 CUSTOS ESPERADOS

- **WhatsApp Business API**: ~R$ 0.005 por mensagem
- **Volume estimado**: 1,000 mensagens/mês
- **Custo mensal**: R$ 5,00
- **Total com APIs de IA**: R$ 349/mês

---

## 🚨 RESOLUÇÃO DE PROBLEMAS

### Problema: "Token inválido"
**Solução**: Gere um novo token de acesso no painel do Meta

### Problema: "Phone Number ID não encontrado"  
**Solução**: Verifique se o número foi verificado corretamente

### Problema: "Webhook não recebe mensagens"
**Solução**: 
1. Verifique se a URL está acessível (HTTPS obrigatório)
2. Confirme se o verify_token está correto
3. Teste o endpoint manualmente

### Problema: "Rate limit excedido"
**Solução**: 
- Aguarde a janela de reset (geralmente 24h)
- Reduza o volume de mensagens
- Considere upgrade do plano

---

## ✅ CHECKLIST FINAL

- [ ] Conta Meta for Developers criada
- [ ] App WhatsApp configurado  
- [ ] Número de telefone verificado
- [ ] ACCESS TOKEN obtido
- [ ] PHONE NUMBER ID identificado
- [ ] BUSINESS ACCOUNT ID coletado
- [ ] Webhook configurado no painel
- [ ] Credenciais inseridas no .env
- [ ] Teste de conectividade aprovado
- [ ] Sistema iniciado e funcionando

---

## 🎯 PRÓXIMOS PASSOS

Após completar esta configuração, seu sistema NatPropTech estará pronto para:

1. **Receber mensagens** do WhatsApp automaticamente
2. **Qualificar leads** usando IA avançada  
3. **Gerar propostas** personalizadas
4. **Acompanhar conversões** em tempo real
5. **Otimizar vendas** com MiniMax M2 Agent

**Sua revolução das vendas imobiliárias começa agora!** 🚀💰