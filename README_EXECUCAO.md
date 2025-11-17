# 🏡 NatPropTech - EXECUÇÃO IMEDIATA

**Guia prático para implementar o projeto em 30 minutos**

---

## 🚀 EXECUÇÃO EM 5 PASSOS

### 1️⃣ **SETUP GOOGLE CLOUD** (10 min)

```bash
# Baixar e executar script de setup
curl -O https://raw.githubusercontent.com/minimax/natproptech/setup_google_cloud.sh
bash setup_google_cloud.sh
```

### 2️⃣ **INSTALAR DEPENDÊNCIAS** (5 min)

```bash
# Criar ambiente virtual
python3 -m venv natproptech-env
source natproptech-env/bin/activate

# Instalar requirements
pip install -r requirements.txt

# Configurar credenciais
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/credentials.json"
export GCP_PROJECT_ID="natproptech-rn"
```

### 3️⃣ **TESTAR LEADCAPTURE AGENT** (5 min)

```bash
# Executar teste
python leadcapture_agent.py
```

### 4️⃣ **INICIAR API FASTAPI** (5 min)

```bash
# Terminal 1: API
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Teste
curl -X POST "http://localhost:8000/api/v1/capture-lead" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao@email.com",
    "phone": "(84) 99999-9999",
    "message": "Quero apartamento 3 quartos, até R$ 450k",
    "source": "whatsapp"
  }'
```

### 5️⃣ **DASHBOARD STREAMLIT** (5 min)

```bash
# Dashboard simples
streamlit run dashboard.py
```

---

## 🧪 TESTES RÁPIDOS

### **Teste 1: Lead Qualificação**
```python
# Python interactivo
from leadcapture_agent import LeadCaptureAgent
import asyncio

async def test():
    agent = LeadCaptureAgent()
    result = await agent.process_lead(
        name="Maria Santos",
        email="maria@email.com",
        phone="(84) 99999-8888",
        message="Interessada em apartamento Natal, 3 quartos, até R$ 400k"
    )
    print(result)

asyncio.run(test())
```

### **Teste 2: API Health Check**
```bash
curl http://localhost:8000/api/v1/health
```

### **Teste 3: BigQuery**
```bash
# Verificar dados salvos
bq query "SELECT name, score, qualification FROM natproptech_data.leads LIMIT 10"
```

---

## 📊 MÉTRICAS ESPERADAS

### **POC (Primeiros 7 dias):**
- 50+ leads processados
- Score médio: 65-75
- Qualificação: 30% hot, 40% warm, 30% cold
- Uptime: 99%+

### **Validação (Semana 2):**
- 5 entrevistas agendadas
- 2 empresas piloto ativas
- Feedback positivo 80%+

### **Captação (Semana 4):**
- Pitch deck finalizado
- 3+ reuniões com investidores
- R$ 1.8M comprometido

---

## 🔧 SOLUÇÃO DE PROBLEMAS

### **Erro: Google Cloud Auth**
```bash
gcloud auth login
gcloud config set project natproptech-rn
```

### **Erro: BigQuery Permission**
```bash
gcloud projects add-iam-policy-binding natproptech-rn \
  --member="user:your-email@gmail.com" \
  --role="roles/bigquery.admin"
```

### **Erro: Gemini API Key**
```python
import os
os.environ["GEMINI_API_KEY"] = "AIzaSyC9qLjzZFMkXa5-821NrYu1Y4LPw8wIbfI"
```

### **Erro: Port 8000 em uso**
```bash
lsof -ti:8000 | xargs kill -9
uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload
```

---

## 📞 CONTATOS

### **Para Suporte Técnico:**
- **WhatsApp:** (84) 9XXXX-XXXX
- **Email:** suporte@natproptech.com.br
- **GitHub:** github.com/natproptech

### **Para Investimentos:**
- **Email:** invest@natproptech.com.br
- **Pitch Deck:** [Link para下载]

### **Para Parcerias:**
- **Email:** parcerias@natproptech.com.br
- **LinkedIn:** NatPropTech

---

## 🎯 PRÓXIMOS PASSOS

### **Semana 1:**
- [x] Setup Google Cloud
- [x] LeadCapture Agent funcionando
- [x] API básica operacional
- [ ] Dashboard Streamlit
- [ ] Testes com 3 usuários

### **Semana 2:**
- [ ] Integração WhatsApp Business
- [ ] Google Forms para leads
- [ ] Zapier para automações
- [ ] 5 entrevistas de validação

### **Semana 3:**
- [ ] Refinamentos baseados em feedback
- [ ] Métricas avançadas
- [ ] Preparação pitch deck
- [ ] Identificação investidores

### **Semana 4:**
- [ ] Pitch deck finalizado
- [ ] Demonstrações para investidores
- [ ] Preparação captação
- [ ] Documentação técnica

---

**🚀 RESULTADO:** Em 30 dias você terá **um POC funcional**, **5 entrevistas agendadas** e **captação preparada** para executar a primeira plataforma de **IA multi-agente** do mercado imobiliário nordestino.

**💪 COMEÇE AGORA!** Execute o primeiro passo: `bash setup_google_cloud.sh`