# 🔧 Códigos de Exemplo - NatPropTech

**Implementação técnica dos principais agentes**

---

## 1. LeadCapture Agent (LeadCaptureAgent.py)

```python
import vertexai
from vertexai.generative_models import GenerativeModel
from google.cloud import bigquery
import google.generativeai as genai

class LeadCaptureAgent:
    def __init__(self, project_id="natproptech-rn"):
        # Initialize Google Cloud services
        vertexai.init(project=project_id, location="us-central1")
        self.model = GenerativeModel("gemini-2.5-pro")
        
        # Initialize BigQuery client
        self.bq_client = bigquery.Client(project=project_id)
        
        # Gemini API setup
        genai.configure(api_key="AIzaSyC9qLjzZFMkXa5-821NrYu1Y4LPw8wIbfI")
        
    async def capture_lead(self, source, data):
        """Capture and qualify lead using AI analysis"""
        try:
            # Extract lead information
            lead_info = {
                'source': source,
                'name': data.get('name', ''),
                'email': data.get('email', ''),
                'phone': data.get('phone', ''),
                'message': data.get('message', ''),
                'behavior_data': data.get('behavior', {}),
                'timestamp': bigquery.ScalarQueryParameter('timestamp', 'TIMESTAMP', 
                                                         datetime.datetime.now())
            }
            
            # Use Gemini for lead qualification
            qualification_prompt = f"""
            Você é um especialista em qualificação de leads para imóveis em Natal RN e Parnamirim RN.
            
            Analise o seguinte lead e forneça um score de 0 a 100:
            
            Nome: {lead_info['name']}
            Email: {lead_info['email']}
            Telefone: {lead_info['phone']}
            Mensagem: {lead_info['message']}
            Fonte: {lead_info['source']}
            Comportamento: {lead_info['behavior_data']}
            
            Critérios de scoring:
            - Qualidade do contato (email/telefone válido)
            - Clareza da intenção de compra
            - Orçamento implícito na mensagem
            - Urgência da necessidade
            - Fonte do lead (WhatsApp > Site > Redes Sociais)
            
            Responda em formato JSON:
            {{
                "score": <0-100>,
                "qualification": "hot/warm/cold",
                "budget_range": "A/B/C",
                "urgency": "high/medium/low",
                "preferred_contact": "whatsapp/email/call",
                "notes": "<análise detalhada>"
            }}
            """
            
            response = await self.model.generate_content_async(qualification_prompt)
            
            # Parse qualification results
            try:
                import json
                qualification = json.loads(response.text)
            except:
                qualification = {
                    "score": 50,
                    "qualification": "warm",
                    "budget_range": "B",
                    "urgency": "medium",
                    "preferred_contact": "whatsapp",
                    "notes": "Análise padrão devido a erro no parsing"
                }
            
            # Store in BigQuery
            await self._store_lead(lead_info, qualification)
            
            return qualification
            
        except Exception as e:
            print(f"Error in lead capture: {str(e)}")
            return None
    
    async def _store_lead(self, lead_info, qualification):
        """Store lead in BigQuery for analytics"""
        query = """
        INSERT INTO natproptech.leads (
            source, name, email, phone, message, score, qualification, 
            budget_range, urgency, preferred_contact, notes, created_at
        ) VALUES (
            @source, @name, @email, @phone, @message, @score, @qualification,
            @budget_range, @urgency, @preferred_contact, @notes, @timestamp
        )
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("source", "STRING", lead_info['source']),
                bigquery.ScalarQueryParameter("name", "STRING", lead_info['name']),
                bigquery.ScalarQueryParameter("email", "STRING", lead_info['email']),
                bigquery.ScalarQueryParameter("phone", "STRING", lead_info['phone']),
                bigquery.ScalarQueryParameter("message", "STRING", lead_info['message']),
                bigquery.ScalarQueryParameter("score", "INTEGER", qualification['score']),
                bigquery.ScalarQueryParameter("qualification", "STRING", qualification['qualification']),
                bigquery.ScalarQueryParameter("budget_range", "STRING", qualification['budget_range']),
                bigquery.ScalarQueryParameter("urgency", "STRING", qualification['urgency']),
                bigquery.ScalarQueryParameter("preferred_contact", "STRING", qualification['preferred_contact']),
                bigquery.ScalarQueryParameter("notes", "STRING", qualification['notes']),
                bigquery.ScalarQueryParameter("timestamp", "TIMESTAMP", lead_info['timestamp'])
            ]
        )
        
        job = self.bq_client.query(query, job_config=job_config)
        await job.result()

    async def analyze_website_behavior(self, session_id, page_data):
        """Analyze user behavior on website"""
        behavior_analysis = {
            'session_id': session_id,
            'pages_visited': page_data.get('pages', []),
            'time_on_site': page_data.get('duration', 0),
            'interactions': page_data.get('interactions', []),
            'device_info': page_data.get('device', {}),
            'location_data': page_data.get('location', {})
        }
        
        prompt = f"""
        Analise o comportamento do usuário no site de imóveis:
        
        Sessão: {session_id}
        Páginas visitadas: {behavior_analysis['pages_visited']}
        Tempo no site: {behavior_analysis['time_on_site']} segundos
        Interações: {behavior_analysis['interactions']}
        
        Baseado no comportamento, qual é o nível de interesse do usuário?
        Considere: tempo gasto, páginas específicas visitadas, interação com formulários, etc.
        
        Responda: high/medium/low
        """
        
        response = await self.model.generate_content_async(prompt)
        interest_level = response.text.strip().lower()
        
        return {
            'interest_level': interest_level,
            'behavior_score': self._calculate_behavior_score(behavior_analysis)
        }
    
    def _calculate_behavior_score(self, behavior_data):
        """Calculate behavior-based score"""
        score = 0
        
        # Time on site
        time_score = min(behavior_data['time_on_site'] / 10, 50)
        score += time_score
        
        # Pages visited
        page_score = min(len(behavior_data['pages_visited']) * 5, 25)
        score += page_score
        
        # Interactions
        interaction_score = min(len(behavior_data['interactions']) * 3, 25)
        score += interaction_score
        
        return min(score, 100)
```

---

## 2. Conversational Sales Agent (SalesAgent.py)

```python
from google.generativeai import GenerativeModel
from google.cloud import firestore
import google.generativeai as genai
from datetime import datetime, timedelta
import json

class ConversationalSalesAgent:
    def __init__(self, project_id="natproptech-rn"):
        genai.configure(api_key="AIzaSyC9qLjzZFMkXa5-821NrYu1Y4LPw8wIbfI")
        
        # Initialize Gemini models
        self.conversational_model = GenerativeModel("gemini-2.5-flash")
        self.planning_model = GenerativeModel("gemini-2.5-pro")
        
        # Initialize Firestore
        self.db = firestore.Client(project=project_id)
        
        # Load context about Natal RN market
        self.market_context = self._load_market_context()
    
    def _load_market_context(self):
        """Load local market knowledge"""
        return """
        Contexto do mercado imobiliário de Natal RN e Parnamirim RN:
        
        Regiões populares:
        - Natal: Ponta Negra, Capim Macio, Tirol, Areia Preta
        - Parnamirim: Centro, Nova Parnamirim, Emaús
        
        Faixas de preço por m² (2025):
        - Ponta Negra: R$ 8.000 - R$ 15.000/m²
        - Capim Macio: R$ 6.000 - R$ 10.000/m²
        - Parnamirim Centro: R$ 4.500 - R$ 8.000/m²
        
        Padrões de comportamento local:
        - Sotaque nordestino predominante
        - Preferência por WhatsApp
        - Família extensa envolvida na decisão
        - Consideração de proximidade ao mar
        """
    
    async def handle_conversation(self, conversation_id, user_message):
        """Handle ongoing conversation with context"""
        try:
            # Get conversation history
            history = await self._get_conversation_history(conversation_id)
            
            # Build conversation context
            context_prompt = f"""
            Você é um assistente de vendas especializado em imóveis de Natal RN e Parnamirim RN.
            
            Contexto do mercado:
            {self.market_context}
            
            Histórico da conversa:
            {history}
            
            Nova mensagem do cliente: "{user_message}"
            
            Responda de forma natural e regional, incorporando:
            1. Expressões características do RN quando apropriado
            2. Conhecimento específico do mercado local
            3. Perguntas qualificadoras naturais
            4. Próximos passos claros
            
            Se for uma pergunta técnica ou de interesse, sugira propriedades específicas
            baseadas na conversa anterior.
            
            Responda em até 150 palavras, mantendo o tom amigável e profissional.
            """
            
            response = await self.conversational_model.generate_content_async(context_prompt)
            
            # Update conversation history
            await self._update_conversation_history(conversation_id, user_message, response.text)
            
            return response.text
            
        except Exception as e:
            print(f"Error in conversation handling: {str(e)}")
            return "Desculpe, tive um problema técnico. Pode reformular sua pergunta?"
    
    async def qualify_prospect(self, conversation_id):
        """Qualify prospect based on conversation analysis"""
        try:
            history = await self._get_conversation_history(conversation_id)
            
            qualification_prompt = f"""
            Analise o histórico da conversa e calcule o score de qualificação:
            
            Histórico:
            {history}
            
            Critérios:
            1. Clareza da necessidade (comprador real vs. curiosos)
            2. Orçamento mencionado ou implícito
            3. Urgência da decisão
            4. Área de interesse (região específica)
            5. Tipo de imóvel preferido
            
            Responda em JSON:
            {{
                "overall_score": <0-100>,
                "need_clarity": <0-100>,
                "budget_mentioned": true/false,
                "estimated_budget": "<faixa de preço>",
                "urgency": "high/medium/low",
                "preferred_area": "<região>",
                "property_type": "<apartamento/casa/terreno>",
                "next_action": "agendar_visita/<específico>",
                "notes": "<observações>"
            }}
            """
            
            response = await self.planning_model.generate_content_async(qualification_prompt)
            
            try:
                import json
                qualification = json.loads(response.text)
            except:
                qualification = {
                    "overall_score": 50,
                    "need_clarity": 50,
                    "budget_mentioned": False,
                    "estimated_budget": "Não informado",
                    "urgency": "medium",
                    "preferred_area": "Natal",
                    "property_type": "Apartamento",
                    "next_action": "agendar_visita",
                    "notes": "Análise padrão"
                }
            
            # Store qualification
            await self._store_qualification(conversation_id, qualification)
            
            return qualification
            
        except Exception as e:
            print(f"Error in qualification: {str(e)}")
            return None
    
    async def suggest_properties(self, user_profile):
        """Suggest properties based on user profile"""
        try:
            suggestion_prompt = f"""
            Com base no perfil do cliente, sugira 3 propriedades específicas:
            
            Perfil:
            - Orçamento: {user_profile.get('budget', 'Não informado')}
            - Área preferida: {user_profile.get('area', 'Natal')}
            - Tipo: {user_profile.get('property_type', 'Apartamento')}
            - Características: {user_profile.get('features', [])}
            
            Use o conhecimento do mercado local para sugerir propriedades reais
            com características específicas de cada região.
            
            Para cada sugestão, forneça:
            1. Descrição da propriedade
            2. Por que combina com o perfil
            3. Vantagens da localização
            4. Próximo passo sugerido
            """
            
            response = await self.planning_model.generate_content_async(suggestion_prompt)
            return response.text
            
        except Exception as e:
            print(f"Error in property suggestion: {str(e)}")
            return None
    
    async def _get_conversation_history(self, conversation_id):
        """Get conversation history from Firestore"""
        try:
            doc = self.db.collection('conversations').document(conversation_id).get()
            if doc.exists:
                return doc.to_dict().get('history', [])
            return []
        except:
            return []
    
    async def _update_conversation_history(self, conversation_id, user_message, response):
        """Update conversation history"""
        try:
            history_data = {
                'history': f"Cliente: {user_message}\nAssistente: {response}",
                'updated_at': datetime.now()
            }
            
            self.db.collection('conversations').document(conversation_id).set(
                history_data, merge=True
            )
        except:
            pass
    
    async def _store_qualification(self, conversation_id, qualification):
        """Store qualification result"""
        try:
            qualification_data = {
                'conversation_id': conversation_id,
                'qualification': qualification,
                'updated_at': datetime.now()
            }
            
            self.db.collection('qualifications').document(conversation_id).set(
                qualification_data
            )
        except:
            pass
```

---

## 3. PropertyMatch Agent (PropertyMatchAgent.py)

```python
import vertexai
from vertexai.generative_models import GenerativeModel
from google.cloud import bigquery
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class PropertyMatchAgent:
    def __init__(self, project_id="natproptech-rn"):
        vertexai.init(project=project_id, location="us-central1")
        self.model = GenerativeModel("gemini-2.5-pro")
        
        # Initialize BigQuery
        self.bq_client = bigquery.Client(project=project_id)
        
        # Initialize vectorizer for property matching
        self.vectorizer = TfidfVectorizer(stop_words='portuguese')
        
        # Load properties database
        self.properties_db = self._load_properties_database()
        
    def _load_properties_database(self):
        """Load properties from BigQuery"""
        query = """
        SELECT 
            id, title, description, price, bedrooms, bathrooms, 
            area, location, neighborhood, amenities, features,
            distance_beach, distance_center, property_type,
            images, virtual_tour_url
        FROM natproptech.properties 
        WHERE status = 'available' AND created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
        """
        
        query_job = self.bq_client.query(query)
        results = query_job.result()
        
        properties = []
        for row in results:
            property_dict = dict(row.items())
            properties.append(property_dict)
        
        return properties
    
    async def match_properties(self, user_profile, preferences):
        """Find best property matches for user"""
        try:
            # Extract user preferences
            budget_min = preferences.get('budget_min', 0)
            budget_max = preferences.get('budget_max', float('inf'))
            bedrooms = preferences.get('bedrooms', 0)
            bathrooms = preferences.get('bathrooms', 0)
            preferred_areas = preferences.get('areas', [])
            property_type = preferences.get('property_type', '')
            must_have_features = preferences.get('must_have', [])
            
            # Filter by basic criteria
            filtered_properties = self._basic_filter(
                budget_min, budget_max, bedrooms, bathrooms, 
                preferred_areas, property_type
            )
            
            # Score properties
            scored_properties = await self._score_properties(filtered_properties, preferences)
            
            # Use AI for final ranking and description
            ranked_properties = await self._ai_ranking(scored_properties, user_profile)
            
            return ranked_properties[:5]  # Top 5 matches
            
        except Exception as e:
            print(f"Error in property matching: {str(e)}")
            return []
    
    def _basic_filter(self, budget_min, budget_max, bedrooms, bathrooms, 
                     preferred_areas, property_type):
        """Apply basic filtering criteria"""
        filtered = []
        
        for prop in self.properties_db:
            # Price filter
            if prop['price'] < budget_min or prop['price'] > budget_max:
                continue
            
            # Bedrooms filter
            if bedrooms > 0 and prop['bedrooms'] < bedrooms:
                continue
            
            # Bathrooms filter
            if bathrooms > 0 and prop['bathrooms'] < bathrooms:
                continue
            
            # Area filter
            if preferred_areas and prop['neighborhood'] not in preferred_areas:
                continue
            
            # Property type filter
            if property_type and prop['property_type'] != property_type:
                continue
            
            filtered.append(prop)
        
        return filtered
    
    async def _score_properties(self, properties, preferences):
        """Score properties based on user preferences"""
        scored = []
        
        for prop in properties:
            score = 0
            
            # Base scoring factors
            score += self._score_price_match(prop, preferences)
            score += self._score_location_match(prop, preferences)
            score += self._score_features_match(prop, preferences)
            score += self._score_amenities_match(prop, preferences)
            
            prop['match_score'] = score
            scored.append(prop)
        
        return sorted(scored, key=lambda x: x['match_score'], reverse=True)
    
    def _score_price_match(self, prop, preferences):
        """Score price alignment with user budget"""
        budget_range = preferences.get('budget_range', {})
        price = prop['price']
        
        if budget_range:
            if price >= budget_range.get('min', 0) and price <= budget_range.get('max', float('inf')):
                return 30  # Perfect price range
            elif price <= budget_range.get('max', float('inf')) * 1.1:
                return 20  # Slightly above budget
            elif price <= budget_range.get('max', float('inf')) * 1.2:
                return 10  # Above budget but acceptable
        
        return 0  # Outside budget
    
    def _score_location_match(self, prop, preferences):
        """Score location preference alignment"""
        preferred_areas = preferences.get('preferred_areas', [])
        neighborhood = prop['neighborhood']
        
        if neighborhood in preferred_areas:
            return 25  # Perfect location match
        elif neighborhood in self._get_similar_areas(preferred_areas):
            return 15  # Similar area
        elif neighborhood in self._get_popular_areas():
            return 10  # Popular area
        else:
            return 5  # Other area
    
    def _get_similar_areas(self, preferred_areas):
        """Get areas similar to user's preferences"""
        similarity_map = {
            'Ponta Negra': ['Capim Macio', 'Tirol'],
            'Capim Macio': ['Ponta Negra', 'Tirol'],
            'Centro': ['Nova Parnamirim'],
            'Nova Parnamirim': ['Centro', 'Emaús']
        }
        
        similar = []
        for area in preferred_areas:
            if area in similarity_map:
                similar.extend(similarity_map[area])
        
        return similar
    
    def _get_popular_areas(self):
        """Get popular areas in the region"""
        return ['Ponta Negra', 'Capim Macio', 'Centro', 'Nova Parnamirim']
    
    def _score_features_match(self, prop, preferences):
        """Score feature alignment"""
        must_have = preferences.get('must_have', [])
        property_features = prop.get('features', [])
        
        if not must_have:
            return 0
        
        matches = len([f for f in must_have if f in property_features])
        return (matches / len(must_have)) * 20
    
    def _score_amenities_match(self, prop, preferences):
        """Score amenities alignment"""
        preferred_amenities = preferences.get('preferred_amenities', [])
        property_amenities = prop.get('amenities', [])
        
        if not preferred_amenities:
            return 0
        
        matches = len([a for a in preferred_amenities if a in property_amenities])
        return (matches / len(preferred_amenities)) * 15
    
    async def _ai_ranking(self, properties, user_profile):
        """Use AI for final ranking and personalization"""
        try:
            # Prepare properties summary for AI
            properties_summary = []
            for prop in properties[:10]:  # Top 10 for AI analysis
                summary = {
                    'id': prop['id'],
                    'title': prop['title'],
                    'price': prop['price'],
                    'bedrooms': prop['bedrooms'],
                    'bathrooms': prop['bathrooms'],
                    'area': prop['area'],
                    'neighborhood': prop['neighborhood'],
                    'score': prop['match_score']
                }
                properties_summary.append(summary)
            
            ranking_prompt = f"""
            Analise estas propriedades e ordene pelo melhor match com o perfil do cliente:
            
            Perfil do cliente:
            {user_profile}
            
            Propriedades candidatas:
            {properties_summary}
            
            Para cada propriedade, forneça:
            1. Justificativa do ranking
            2. Vantagens específicas para este cliente
            3. Possíveis desvantagens a mencionar
            4. Próximo passo sugerido
            
            Responda em formato JSON com o ranking final:
            [
                {{
                    "property_id": "<id>",
                    "rank": <1-10>,
                    "justification": "<explicação>",
                    "advantages": ["<vantagem1>", "<vantagem2>"],
                    "disadvantages": ["<desvantagem1>"],
                    "next_step": "<ação sugerida>"
                }}
            ]
            """
            
            response = await self.model.generate_content_async(ranking_prompt)
            
            try:
                import json
                ai_ranking = json.loads(response.text)
            except:
                ai_ranking = []
            
            # Merge AI ranking with original scoring
            final_ranking = []
            for rank_item in ai_ranking:
                property_id = rank_item['property_id']
                original_prop = next((p for p in properties if str(p['id']) == str(property_id)), None)
                if original_prop:
                    original_prop['ai_ranking'] = rank_item
                    final_ranking.append(original_prop)
            
            return final_ranking
            
        except Exception as e:
            print(f"Error in AI ranking: {str(e)}")
            return properties
    
    def calculate_match_percentage(self, property_data, user_profile):
        """Calculate overall match percentage"""
        try:
            # Use vector similarity for text matching
            property_text = f"{property_data['description']} {property_data['amenities']}"
            user_text = f"{user_profile['preferences']} {user_profile['must_have']}"
            
            if not user_text.strip():
                return 50  # Default score if no preferences
            
            # Simple text similarity
            vectorizer = TfidfVectorizer()
            try:
                vectors = vectorizer.fit_transform([property_text, user_text])
                similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
                return int(similarity * 100)
            except:
                return 50
                
        except Exception as e:
            print(f"Error calculating match percentage: {str(e)}")
            return 50
```

---

## 4. Analytics Agent (AnalyticsAgent.py)

```python
from google.cloud import bigquery
from google.cloud import monitoring_v3
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

class AnalyticsAgent:
    def __init__(self, project_id="natproptech-rn"):
        self.bq_client = bigquery.Client(project=project_id)
        self.monitoring_client = monitoring_v3.MetricServiceClient()
        
        # Setup matplotlib for visualization
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
    async def generate_market_insights(self, period_days=30):
        """Generate comprehensive market insights"""
        try:
            insights = {}
            
            # Sales performance analysis
            insights['sales_performance'] = await self._analyze_sales_performance(period_days)
            
            # Lead conversion analysis
            insights['lead_conversion'] = await self._analyze_lead_conversion(period_days)
            
            # Market trends
            insights['market_trends'] = await self._analyze_market_trends(period_days)
            
            # Regional performance
            insights['regional_performance'] = await self._analyze_regional_performance(period_days)
            
            # Predictive analytics
            insights['predictions'] = await self._generate_predictions(period_days)
            
            return insights
            
        except Exception as e:
            print(f"Error generating market insights: {str(e)}")
            return {}
    
    async def _analyze_sales_performance(self, period_days):
        """Analyze sales performance metrics"""
        query = f"""
        SELECT 
            DATE(created_at) as sale_date,
            COUNT(*) as total_sales,
            SUM(value) as total_value,
            AVG(value) as avg_sale_value,
            COUNT(DISTINCT customer_id) as unique_customers
        FROM natproptech.sales
        WHERE created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL {period_days} DAY)
        GROUP BY DATE(created_at)
        ORDER BY sale_date
        """
        
        query_job = self.bq_client.query(query)
        results = query_job.result()
        
        sales_data = [dict(row.items()) for row in results]
        
        # Calculate performance metrics
        if sales_data:
            total_sales = sum([row['total_sales'] for row in sales_data])
            total_value = sum([row['total_value'] for row in sales_data])
            avg_daily_sales = total_sales / period_days
            
            return {
                'total_sales': total_sales,
                'total_value': total_value,
                'avg_daily_sales': avg_daily_sales,
                'daily_breakdown': sales_data,
                'performance_trend': self._calculate_trend(sales_data, 'total_sales')
            }
        
        return {'total_sales': 0, 'total_value': 0, 'avg_daily_sales': 0}
    
    async def _analyze_lead_conversion(self, period_days):
        """Analyze lead conversion funnel"""
        query = f"""
        WITH funnel_data AS (
            SELECT 
                source,
                qualification,
                COUNT(*) as lead_count,
                COUNT(CASE WHEN qualification IN ('hot', 'warm') THEN 1 END) as qualified_leads,
                COUNT(CASE WHEN converted = true THEN 1 END) as converted_leads
            FROM natproptech.leads
            WHERE created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL {period_days} DAY)
            GROUP BY source, qualification
        )
        SELECT 
            source,
            SUM(lead_count) as total_leads,
            SUM(qualified_leads) as total_qualified,
            SUM(converted_leads) as total_converted,
            SAFE_DIVIDE(SUM(qualified_leads), SUM(lead_count)) * 100 as qualification_rate,
            SAFE_DIVIDE(SUM(converted_leads), SUM(qualified_leads)) * 100 as conversion_rate
        FROM funnel_data
        GROUP BY source
        ORDER BY total_leads DESC
        """
        
        query_job = self.bq_client.query(query)
        results = query_job.result()
        
        conversion_data = [dict(row.items()) for row in results]
        
        return {
            'conversion_funnel': conversion_data,
            'best_source': max(conversion_data, key=lambda x: x['conversion_rate']) if conversion_data else None,
            'total_leads': sum([row['total_leads'] for row in conversion_data]),
            'overall_conversion_rate': sum([row['total_converted'] for row in conversion_data]) / 
                                      max(sum([row['total_leads'] for row in conversion_data]), 1) * 100
        }
    
    async def _analyze_market_trends(self, period_days):
        """Analyze market trends and patterns"""
        query = f"""
        SELECT 
            neighborhood,
            property_type,
            AVG(price) as avg_price,
            AVG(price_per_sqm) as avg_price_per_sqm,
            COUNT(*) as property_count,
            AVG(days_on_market) as avg_days_on_market
        FROM natproptech.properties
        WHERE created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL {period_days} DAY)
        AND status = 'sold'
        GROUP BY neighborhood, property_type
        ORDER BY avg_price_per_sqm DESC
        """
        
        query_job = self.bq_client.query(query)
        results = query_job.result()
        
        market_trends = [dict(row.items()) for row in results]
        
        # Calculate trend indicators
        trends_analysis = {
            'most_expensive_area': max(market_trends, key=lambda x: x['avg_price_per_sqm']) if market_trends else None,
            'fastest_selling_area': min(market_trends, key=lambda x: x['avg_days_on_market']) if market_trends else None,
            'market_data': market_trends
        }
        
        return trends_analysis
    
    async def _analyze_regional_performance(self, period_days):
        """Analyze performance by region"""
        query = f"""
        SELECT 
            l.neighborhood,
            COUNT(l.id) as total_leads,
            COUNT(CASE WHEN l.converted = true THEN 1 END) as conversions,
            AVG(l.score) as avg_lead_score,
            AVG(p.price) as avg_property_price
        FROM natproptech.leads l
        LEFT JOIN natproptech.properties p ON l.property_id = p.id
        WHERE l.created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL {period_days} DAY)
        GROUP BY l.neighborhood
        ORDER BY conversions DESC
        """
        
        query_job = self.bq_client.query(query)
        results = query_job.result()
        
        regional_data = [dict(row.items()) for row in results]
        
        return {
            'regional_breakdown': regional_data,
            'top_performing_area': max(regional_data, key=lambda x: x['conversions']) if regional_data else None
        }
    
    async def _generate_predictions(self, period_days):
        """Generate predictive analytics"""
        # Use recent data for trend prediction
        historical_query = f"""
        SELECT 
            DATE(created_at) as date,
            COUNT(*) as daily_sales
        FROM natproptech.sales
        WHERE created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL {period_days * 2} DAY)
        AND created_at < DATE_SUB(CURRENT_DATE(), INTERVAL {period_days} DAY)
        GROUP BY DATE(created_at)
        ORDER BY date
        """
        
        query_job = self.bq_client.query(historical_query)
        results = query_job.result()
        
        historical_data = [dict(row.items()) for row in results]
        
        # Simple linear trend prediction
        if len(historical_data) >= 7:
            predictions = self._calculate_linear_prediction(historical_data, period_days)
            return {
                'sales_prediction': predictions['sales'],
                'trend_direction': predictions['direction'],
                'confidence_level': predictions['confidence']
            }
        
        return {'sales_prediction': {}, 'trend_direction': 'stable', 'confidence_level': 'low'}
    
    def _calculate_linear_prediction(self, historical_data, forecast_days):
        """Calculate linear trend prediction"""
        try:
            import numpy as np
            
            dates = [datetime.strptime(row['date'], '%Y-%m-%d') for row in historical_data]
            sales = [row['daily_sales'] for row in historical_data]
            
            # Simple linear regression
            x = np.arange(len(dates))
            y = np.array(sales)
            
            # Calculate trend
            if len(x) > 1:
                slope, intercept = np.polyfit(x, y, 1)
                
                # Predict future values
                future_x = np.arange(len(dates), len(dates) + forecast_days)
                future_sales = slope * future_x + intercept
                
                return {
                    'sales': future_sales.tolist(),
                    'direction': 'increasing' if slope > 0 else 'decreasing',
                    'confidence': 'high' if abs(slope) > 0.1 else 'medium'
                }
        except:
            pass
        
        return {
            'sales': [sales[-1]] * forecast_days,
            'direction': 'stable',
            'confidence': 'low'
        }
    
    def _calculate_trend(self, data, metric):
        """Calculate trend direction for a metric"""
        if len(data) < 2:
            return 'stable'
        
        recent_values = [row[metric] for row in data[-7:]]  # Last 7 days
        older_values = [row[metric] for row in data[-14:-7]]  # Previous 7 days
        
        if recent_values and older_values:
            recent_avg = sum(recent_values) / len(recent_values)
            older_avg = sum(older_values) / len(older_values)
            
            if recent_avg > older_avg * 1.1:
                return 'increasing'
            elif recent_avg < older_avg * 0.9:
                return 'decreasing'
        
        return 'stable'
    
    async def create_dashboard_metrics(self):
        """Create key metrics for dashboard"""
        try:
            # Get current month data
            current_month_query = """
            SELECT 
                COUNT(*) as total_leads,
                COUNT(CASE WHEN qualification IN ('hot', 'warm') THEN 1 END) as qualified_leads,
                COUNT(CASE WHEN converted = true THEN 1 END) as conversions,
                AVG(score) as avg_lead_score
            FROM natproptech.leads
            WHERE EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM CURRENT_DATE())
            AND EXTRACT(MONTH FROM created_at) = EXTRACT(MONTH FROM CURRENT_DATE())
            """
            
            query_job = self.bq_client.query(current_month_query)
            results = query_job.result()
            month_data = dict(next(results).items())
            
            # Calculate conversion rates
            conversion_rate = (month_data['conversions'] / month_data['total_leads'] * 100) if month_data['total_leads'] > 0 else 0
            qualification_rate = (month_data['qualified_leads'] / month_data['total_leads'] * 100) if month_data['total_leads'] > 0 else 0
            
            return {
                'monthly_leads': month_data['total_leads'],
                'monthly_conversions': month_data['conversions'],
                'conversion_rate': round(conversion_rate, 2),
                'qualification_rate': round(qualification_rate, 2),
                'avg_lead_score': round(month_data['avg_lead_score'] or 0, 2)
            }
            
        except Exception as e:
            print(f"Error creating dashboard metrics: {str(e)}")
            return {}
```

---

## 5. Main Orchestrator (main.py)

```python
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from LeadCaptureAgent import LeadCaptureAgent
from SalesAgent import ConversationalSalesAgent
from PropertyMatchAgent import PropertyMatchAgent
from AnalyticsAgent import AnalyticsAgent
from google.cloud import firestore
import uvicorn

app = FastAPI(title="NatPropTech Multi-Agent System")

# Initialize agents
lead_agent = LeadCaptureAgent()
sales_agent = ConversationalSalesAgent()
match_agent = PropertyMatchAgent()
analytics_agent = AnalyticsAgent()

# Pydantic models
class LeadCaptureRequest(BaseModel):
    source: str
    name: str
    email: str
    phone: str
    message: str
    behavior: Optional[Dict[str, Any]] = {}

class ConversationRequest(BaseModel):
    conversation_id: str
    user_message: str

class PropertyMatchRequest(BaseModel):
    user_profile: Dict[str, Any]
    preferences: Dict[str, Any]

@app.post("/api/lead/capture")
async def capture_lead(request: LeadCaptureRequest):
    """Capture and qualify new lead"""
    try:
        result = await lead_agent.capture_lead(request.source, request.dict())
        return {"status": "success", "qualification": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sales/chat")
async def handle_conversation(request: ConversationRequest):
    """Handle conversation with sales agent"""
    try:
        response = await sales_agent.handle_conversation(
            request.conversation_id, 
            request.user_message
        )
        return {"status": "success", "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/properties/match")
async def match_properties(request: PropertyMatchRequest):
    """Find property matches for user"""
    try:
        matches = await match_agent.match_properties(
            request.user_profile, 
            request.preferences
        )
        return {"status": "success", "matches": matches}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/insights")
async def get_market_insights():
    """Get comprehensive market insights"""
    try:
        insights = await analytics_agent.generate_market_insights()
        return {"status": "success", "insights": insights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/dashboard/metrics")
async def get_dashboard_metrics():
    """Get dashboard metrics"""
    try:
        metrics = await analytics_agent.create_dashboard_metrics()
        return {"status": "success", "metrics": metrics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

---

## 🚀 Como Executar

### 1. Setup do Ambiente
```bash
# Instalar dependências
pip install google-cloud-vertexai google-generativeai google-cloud-bigquery
pip install google-cloud-firestore google-cloud-monitoring-v3
pip install fastapi uvicorn scikit-learn pandas matplotlib seaborn

# Configurar variáveis de ambiente
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"
export GEMINI_API_KEY="AIzaSyC9qLjzZFMkXa5-821NrYu1Y4LPw8wIbfI"
```

### 2. Deploy no Google Cloud Run
```bash
# Build e deploy
gcloud run deploy natproptech-api \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

### 3. Integração com Frontend
```javascript
// Exemplo de integração com React
const captureLead = async (leadData) => {
  const response = await fetch('/api/lead/capture', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(leadData)
  });
  return await response.json();
};

const chatWithSales = async (conversationId, message) => {
  const response = await fetch('/api/sales/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ conversation_id: conversationId, user_message: message })
  });
  return await response.json();
};
```

Este código fornece uma base sólida para implementação da plataforma NatPropTech com arquitetura multi-agente completa!