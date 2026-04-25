#!/usr/bin/env bash
# Script para configurar GitHub Secrets automáticamente
# Requiere GitHub CLI instalado: https://cli.github.com

set -e

echo "🔐 Configurando GitHub Secrets para CI/CD..."
echo ""

# Verificar que gh está instalado
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI no está instalado"
    echo "Instálalo desde: https://cli.github.com"
    exit 1
fi

echo "✅ GitHub CLI detectado"
echo ""

# Verificar que está autenticado
if ! gh auth status &> /dev/null; then
    echo "❌ No estás autenticado en GitHub"
    echo "Ejecuta: gh auth login"
    exit 1
fi

echo "✅ Autenticado en GitHub"
echo ""

# Obtener repo info
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
echo "📦 Configurando secretos para: $REPO"
echo ""

# Función para configurar secreto
set_secret() {
    local secret_name=$1
    local secret_value=$2
    local description=$3
    
    echo "Setting: $secret_name"
    echo "$secret_value" | gh secret set "$secret_name" --repo "$REPO"
    echo "  ✅ $description"
}

# Railway Token
echo "🎫 Necesito tu Railway Token"
read -p "Ingresa tu RAILWAY_TOKEN (desde https://railway.app/account/tokens): " railway_token
set_secret "RAILWAY_TOKEN" "$railway_token" "Railway authentication token"
echo ""

# Railway Service IDs
echo "🚂 Railway Service IDs"
echo "Puedes obtenerlos de:"
echo "1. Accede a Railway → Tu proyecto"
echo "2. Click en cada servicio"
echo "3. En la URL: https://railway.app/project/<PROJECT_ID>/service/<SERVICE_ID>"
echo ""

read -p "Backend Service ID (DEV): " backend_dev_id
set_secret "RAILWAY_BACKEND_SERVICE_ID" "$backend_dev_id" "Development backend service"
echo ""

read -p "Frontend Service ID (DEV): " frontend_dev_id
set_secret "RAILWAY_FRONTEND_SERVICE_ID" "$frontend_dev_id" "Development frontend service"
echo ""

# URLs
echo "🌐 URLs de ambiente"
read -p "DEV API URL (ej: https://bus-backend-dev-xxx.up.railway.app): " dev_url
set_secret "DEV_API_URL" "$dev_url" "Development API URL"
echo ""

# Staging (opcional)
read -p "¿Configurar Staging? (s/n): " staging_response
if [[ $staging_response =~ ^[Ss]$ ]]; then
    read -p "Staging Backend Service ID: " staging_backend_id
    set_secret "RAILWAY_STAGING_BACKEND_SERVICE_ID" "$staging_backend_id" "Staging backend service"
    
    read -p "Staging Frontend Service ID: " staging_frontend_id
    set_secret "RAILWAY_STAGING_FRONTEND_SERVICE_ID" "$staging_frontend_id" "Staging frontend service"
    
    read -p "Staging API URL: " staging_url
    set_secret "STAGING_API_URL" "$staging_url" "Staging API URL"
    echo ""
fi

# Production (opcional)
read -p "¿Configurar Production? (s/n): " prod_response
if [[ $prod_response =~ ^[Ss]$ ]]; then
    read -p "Production Backend Service ID: " prod_backend_id
    set_secret "RAILWAY_PROD_BACKEND_SERVICE_ID" "$prod_backend_id" "Production backend service"
    
    read -p "Production Frontend Service ID: " prod_frontend_id
    set_secret "RAILWAY_PROD_FRONTEND_SERVICE_ID" "$prod_frontend_id" "Production frontend service"
    
    read -p "Production API URL: " prod_url
    set_secret "PROD_API_URL" "$prod_url" "Production API URL"
    echo ""
fi

# Slack Webhook (opcional)
read -p "¿Agregar Slack webhook para notificaciones? (s/n): " slack_response
if [[ $slack_response =~ ^[Ss]$ ]]; then
    read -p "Slack Webhook URL: " slack_webhook
    set_secret "SLACK_WEBHOOK" "$slack_webhook" "Slack webhook for notifications"
    echo ""
fi

echo "═══════════════════════════════════════"
echo "✅ GitHub Secrets configurados!"
echo "═══════════════════════════════════════"
echo ""
echo "Puedes ver los secretos en:"
echo "https://github.com/$REPO/settings/secrets/actions"
echo ""
echo "🎉 CI/CD está listo para usar!"
