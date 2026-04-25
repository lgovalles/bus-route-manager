#!/bin/bash
# Script para subir bus-route-manager a GitHub
# Este script automatiza todos los pasos

set -e  # Exit si hay error

echo "🚀 Iniciando setup de GitHub para Bus Route Manager..."
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Paso 1: Validar que estamos en la carpeta correcta
if [ ! -f "README.md" ]; then
    echo -e "${RED}❌ Error: Debe ejecutar este script desde la raíz del proyecto${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Estamos en la carpeta correcta${NC}"
echo ""

# Paso 2: Configurar git globalmente
echo "📝 Configurando git..."
read -p "¿Cuál es tu nombre? " git_name
read -p "¿Cuál es tu email de GitHub? " git_email

git config --global user.name "$git_name"
git config --global user.email "$git_email"

echo -e "${GREEN}✅ Git configurado${NC}"
echo ""

# Paso 3: Inicializar repositorio
if [ -d ".git" ]; then
    echo -e "${YELLOW}⚠️ Git repository ya existe, saltando init${NC}"
else
    echo "🔧 Inicializando git repository..."
    git init
    git branch -M main
    echo -e "${GREEN}✅ Repository inicializado${NC}"
fi
echo ""

# Paso 4: Agregar archivos
echo "📦 Agregando archivos..."
git add .
echo -e "${GREEN}✅ Archivos agregados${NC}"
echo ""

# Paso 5: Verificar status
echo "📋 Status actual:"
git status
echo ""

# Paso 6: Commit inicial
read -p "¿Proceder con el commit inicial? (s/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    git commit -m "🚀 Initial commit: Bus Route Manager - FastAPI + React

- Backend: FastAPI REST API with pytest, Ruff
- Frontend: React 18 + TypeScript with Vitest + Playwright
- Infrastructure: Docker + GitHub Actions CI/CD ready
- Database: PostgreSQL support
- Deployment: Railway ready"
    echo -e "${GREEN}✅ Commit realizado${NC}"
else
    echo -e "${YELLOW}⚠️ Commit cancelado${NC}"
    exit 1
fi
echo ""

# Paso 7: Conectar con remote
read -p "¿Cuál es tu usuario de GitHub? " github_user
repo_url="https://github.com/${github_user}/bus-route-manager.git"

echo "🔗 Agregando remote: $repo_url"
git remote add origin "$repo_url" || git remote set-url origin "$repo_url"
git remote -v
echo -e "${GREEN}✅ Remote configurado${NC}"
echo ""

# Paso 8: Push
echo "📤 Subiendo a GitHub..."
echo -e "${YELLOW}Nota: Si es la primera vez, se te pedirá autenticación${NC}"
git push -u origin main

echo -e "${GREEN}✅ ¡Proyecto subido a GitHub!${NC}"
echo ""

# Paso 9: Verificar
echo "🔍 Verificando..."
git log --oneline -n 3
echo ""

echo -e "${GREEN}═════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Setup completado exitosamente!${NC}"
echo -e "${GREEN}═════════════════════════════════════════${NC}"
echo ""
echo "📖 Próximos pasos:"
echo "1. Accede a GitHub: https://github.com/$github_user/bus-route-manager"
echo "2. Configura GitHub Secrets (Settings → Secrets)"
echo "3. Lee: docs/RAILWAY_SETUP.md para configurar deployment"
echo "4. Lee: docs/CICD_STRATEGY.md para entender los pipelines"
echo ""
echo "🎉 ¡Ahora tienes CI/CD listo con GitHub Actions!"
