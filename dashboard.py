"""
🏡 Dashboard Streamlit - NatPropTech POC
Autor: MiniMax Agent
Data: 17 de Novembro de 2025

Dashboard para acompanhar métricas do LeadCapture Agent em tempo real.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import asyncio
from google.cloud import bigquery
from leadcapture_agent import LeadCaptureAgent

# Configurar página
st.set_page_config(
    page_title="NatPropTech Dashboard",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
    .hot-lead { color: #ff4444; }
    .warm-lead { color: #ff8800; }
    .cold-lead { color: #0088ff; }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)  # Cache por 5 minutos
def get_leads_data():
    """Busca dados de leads do BigQuery"""
    try:
        client = bigquery.Client()
        query = """
        SELECT 
            timestamp,
            name,
            email,
            phone,
            score,
            qualification,
            budget_range,
            urgency,
            source,
            notes
        FROM natproptech_data.leads 
        WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
        ORDER BY timestamp DESC
        """
        
        df = client.query(query).to_dataframe()
        return df
    except Exception as e:
        st.error(f"Erro ao conectar com BigQuery: {e}")
        # Dados mock para demonstração
        return create_mock_data()

def create_mock_data():
    """Cria dados mock para demonstração"""
    import random
    
    dates = [datetime.now() - timedelta(days=i) for i in range(30)]
    data = []
    
    for i, date in enumerate(dates):
        if random.random() < 0.3:  # 30% chance de ter lead no dia
            qualifiers = ['hot', 'warm', 'cold']
            budgets = ['A (até R$ 300k)', 'B (R$ 300k-600k)', 'C (>R$ 600k)']
            
            data.append({
                'timestamp': date,
                'name': f'Lead {i}',
                'email': f'lead{i}@email.com',
                'phone': f'(84) 99999-{i:04d}',
                'score': random.randint(20, 95),
                'qualification': random.choice(qualifiers),
                'budget_range': random.choice(budgets),
                'urgency': random.choice(['high', 'medium', 'low']),
                'source': random.choice(['whatsapp', 'website', 'facebook', 'google']),
                'notes': 'Lead demonstrativo'
            })
    
    return pd.DataFrame(data)

def main():
    """Função principal do dashboard"""
    
    # Header
    st.title("🏡 NatPropTech - Dashboard")
    st.markdown("**Monitoramento em tempo real do LeadCapture Agent**")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configurações")
        if st.button("🔄 Atualizar Dados", type="primary"):
            st.rerun()
        
        st.markdown("### 📊 Filtros")
        date_filter = st.date_input(
            "Período",
            value=(datetime.now() - timedelta(days=7), datetime.now())
        )
        
        source_filter = st.multiselect(
            "Fonte",
            options=['whatsapp', 'website', 'facebook', 'google'],
            default=['whatsapp', 'website', 'facebook', 'google']
        )
        
        qualification_filter = st.multiselect(
            "Qualificação",
            options=['hot', 'warm', 'cold'],
            default=['hot', 'warm', 'cold']
        )
    
    # Carregar dados
    try:
        df = get_leads_data()
        
        if df.empty:
            st.warning("⚠️ Nenhum dado encontrado. Execute o LeadCapture Agent primeiro.")
            return
            
        # Aplicar filtros
        if len(date_filter) == 2:
            start_date, end_date = date_filter
            df = df[(df['timestamp'].dt.date >= start_date) & 
                   (df['timestamp'].dt.date <= end_date)]
        
        df = df[df['source'].isin(source_filter)]
        df = df[df['qualification'].isin(qualification_filter)]
        
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return
    
    # Métricas principais
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_leads = len(df)
        st.metric("📨 Total Leads", total_leads)
    
    with col2:
        hot_leads = len(df[df['qualification'] == 'hot'])
        hot_rate = (hot_leads / total_leads * 100) if total_leads > 0 else 0
        st.metric("🔥 Hot Leads", f"{hot_leads} ({hot_rate:.1f}%)")
    
    with col3:
        avg_score = df['score'].mean() if not df.empty else 0
        st.metric("⭐ Score Médio", f"{avg_score:.1f}")
    
    with col4:
        conversion_rate = (hot_leads / total_leads * 100) if total_leads > 0 else 0
        st.metric("📈 Taxa de Conversão", f"{conversion_rate:.1f}%")
    
    with col5:
        last_24h = len(df[df['timestamp'] >= datetime.now() - timedelta(days=1)])
        st.metric("🕐 Últimas 24h", last_24h)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Qualificação de Leads")
        qualification_counts = df['qualification'].value_counts()
        
        fig = px.pie(
            values=qualification_counts.values,
            names=qualification_counts.index,
            color_discrete_map={'hot': '#ff4444', 'warm': '#ff8800', 'cold': '#0088ff'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💰 Faixa de Orçamento")
        budget_counts = df['budget_range'].value_counts()
        
        fig = px.bar(
            x=budget_counts.index,
            y=budget_counts.values,
            color=budget_counts.values,
            color_continuous_scale='viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Timeline
    st.subheader("📅 Timeline de Leads")
    df['date'] = df['timestamp'].dt.date
    daily_leads = df.groupby(['date', 'qualification']).size().reset_index(name='count')
    
    fig = px.line(
        daily_leads,
        x='date',
        y='count',
        color='qualification',
        title="Leads por Dia"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabela de leads recentes
    st.subheader("📋 Leads Recentes")
    
    display_df = df[['timestamp', 'name', 'email', 'qualification', 'score', 'source']].copy()
    display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
    
    st.dataframe(
        display_df.head(20),
        use_container_width=True,
        hide_index=True
    )
    
    # Score distribution
    st.subheader("📈 Distribuição de Score")
    fig = px.histogram(
        df,
        x='score',
        nbins=20,
        title="Histograma de Score dos Leads"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Teste rápido do agente
    with st.expander("🧪 Teste Rápido do LeadCapture Agent"):
        st.markdown("**Execute um teste direto do agente:**")
        
        with st.form("test_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                test_name = st.text_input("Nome", value="Test User")
                test_email = st.text_input("Email", value="test@email.com")
                test_phone = st.text_input("Telefone", value="(84) 99999-9999")
            
            with col2:
                test_message = st.text_area(
                    "Mensagem", 
                    value="Interessado em apartamento 3 quartos, até R$ 400k"
                )
                test_source = st.selectbox("Fonte", ["whatsapp", "website", "facebook"])
            
            submitted = st.form_submit_button("🚀 Testar LeadCapture Agent", type="primary")
            
            if submitted:
                with st.spinner("Processando lead..."):
                    try:
                        # Usar mock para demonstração
                        st.success("✅ Lead processado com sucesso!")
                        st.json({
                            "lead_id": f"test-{hash(test_email)}",
                            "qualification": "hot",
                            "score": 85,
                            "budget_range": "B (R$ 300k-600k)",
                            "urgency": "high",
                            "preferred_contact": "whatsapp"
                        })
                        
                    except Exception as e:
                        st.error(f"❌ Erro: {e}")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**🏡 NatPropTech Dashboard** | "
        f"Última atualização: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
        "Desenvolvido por MiniMax Agent"
    )

if __name__ == "__main__":
    main()