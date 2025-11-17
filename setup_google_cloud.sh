#!/bin/bash

# 🚀 SETUP GOOGLE CLOUD - NatPropTech
# Autor: MiniMax Agent
# Data: 17 de Novembro de 2025

echo "🏡 INICIANDO SETUP NATPROPTECH - GOOGLE CLOUD"
echo "================================================"

# Verificar se Google Cloud CLI está instalado
if ! command -v gcloud &> /dev/null; then
    echo "📦 Instalando Google Cloud CLI..."
    curl https://sdk.cloud.google.com | bash
    exec -l $SHELL
else
    echo "✅ Google Cloud CLI já instalado"
fi

# Login no Google Cloud
echo "🔐 Fazendo login no Google Cloud..."
gcloud auth login

# Configurar projeto
PROJECT_ID="natproptech-rn"
echo "🏗️ Criando projeto $PROJECT_ID..."

# Criar projeto se não existir
if ! gcloud projects describe $PROJECT_ID &> /dev/null; then
    gcloud projects create $PROJECT_ID --name="NatPropTech RN"
    echo "✅ Projeto $PROJECT_ID criado com sucesso"
else
    echo "✅ Projeto $PROJECT_ID já existe"
fi

# Definir projeto como padrão
gcloud config set project $PROJECT_ID

# Habilitar APIs necessárias
echo "🔌 Habilitando APIs necessárias..."
APIS=(
    "aiplatform.googleapis.com"
    "bigquery.googleapis.com"
    "cloudbuild.googleapis.com"
    "run.googleapis.com"
    "storage.googleapis.com"
    "cloudresourcemanager.googleapis.com"
)

for api in "${APIS[@]}"; do
    echo "  - Habilitando $api..."
    gcloud services enable $api
done

# Criar Service Account
SERVICE_ACCOUNT="natproptech-sa"
echo "👤 Criando Service Account $SERVICE_ACCOUNT..."

if ! gcloud iam service-accounts describe $SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com &> /dev/null; then
    gcloud iam service-accounts create $SERVICE_ACCOUNT \
        --description="Service Account para NatPropTech" \
        --display-name="NatPropTech-SA"
    echo "✅ Service Account criado"
else
    echo "✅ Service Account já existe"
fi

# Atribuir permissões
echo "🔐 Configurando permissões..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/bigquery.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

# Criar chave JSON
KEY_FILE="credentials.json"
echo "🔑 Gerando chave de credenciais..."
gcloud iam service-accounts keys create $KEY_FILE \
    --iam-account=$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com \
    --key-file-type=json

echo "✅ Chave salva em $KEY_FILE"

# Configurar variáveis de ambiente
echo "⚙️ Configurando variáveis de ambiente..."
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/$KEY_FILE"
export GCP_PROJECT_ID="$PROJECT_ID"

# Criar Dataset BigQuery
echo "🗃️ Configurando BigQuery..."
DATASET="natproptech_data"

# Criar dataset
bq mk --location=US $DATASET

# Criar tabela de leads
bq mk -t --schema=timestamp:TIMESTAMP,name:STRING,email:STRING,phone:STRING,score:INTEGER,qualification:STRING,budget_range:STRING,urgency:STRING,notes:STRING,source:STRING,raw_qualification:STRING $DATASET.leads

# Criar tabela de propriedades
bq mk -t --schema=property_id:STRING,name:STRING,location:STRING,price:INTEGER,bedrooms:INTEGER,area:FLOAT,status:STRING,description:STRING $DATASET.properties

# Criar tabela de analytics
bq mk -t --schema=date:DATE,total_leads:INTEGER,hot_leads:INTEGER,conversion_rate:FLOAT,avg_score:FLOAT,revenue:FLOAT $DATASET.analytics

echo "✅ BigQuery configurado com sucesso"

# Mostrar resumo final
echo ""
echo "🎉 SETUP CONCLUÍDO COM SUCESSO!"
echo "================================"
echo "📊 Projeto ID: $PROJECT_ID"
echo "🔑 Credenciais: $KEY_FILE"
echo "🗃️ Dataset BigQuery: $DATASET"
echo "📋 Service Account: $SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com"
echo ""
echo "📝 Próximos passos:"
echo "1. Execute: export GOOGLE_APPLICATION_CREDENTIALS=$(pwd)/$KEY_FILE"
echo "2. Execute: export GCP_PROJECT_ID=$PROJECT_ID"
echo "3. Execute o LeadCapture Agent para testar"
echo ""
echo "🚀 Your NatPropTech está pronto para uso!"

# Salvar configurações em arquivo
echo "project_id=$PROJECT_ID" > .natproptech-config
echo "service_account=$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com" >> .natproptech-config
echo "dataset_id=$DATASET" >> .natproptech-config
echo "credentials_file=$KEY_FILE" >> .natproptech-config

echo "⚙️ Configurações salvas em .natproptech-config"