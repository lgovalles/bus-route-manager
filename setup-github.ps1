# Script PowerShell para subir bus-route-manager a GitHub
# Ejecuta desde la raíz del proyecto

$ErrorActionPreference = "Stop"

Write-Host "🚀 Iniciando setup de GitHub para Bus Route Manager..." -ForegroundColor Green
Write-Host ""

# Paso 1: Validar que estamos en la carpeta correcta
if (-not (Test-Path "README.md")) {
    Write-Host "❌ Error: Debe ejecutar este script desde la raíz del proyecto" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Estamos en la carpeta correcta" -ForegroundColor Green
Write-Host ""

# Paso 2: Configurar git globalmente
Write-Host "📝 Configurando git..." -ForegroundColor Yellow
$gitName = Read-Host "¿Cuál es tu nombre?"
$gitEmail = Read-Host "¿Cuál es tu email de GitHub?"

git config --global user.name $gitName
git config --global user.email $gitEmail

Write-Host "✅ Git configurado" -ForegroundColor Green
Write-Host ""

# Paso 3: Inicializar repositorio
if (Test-Path ".git") {
    Write-Host "⚠️ Git repository ya existe, saltando init" -ForegroundColor Yellow
}
else {
    Write-Host "🔧 Inicializando git repository..." -ForegroundColor Yellow
    git init
    git branch -M main
    Write-Host "✅ Repository inicializado" -ForegroundColor Green
}
Write-Host ""

# Paso 4: Agregar archivos
Write-Host "📦 Agregando archivos..." -ForegroundColor Yellow
git add .
Write-Host "✅ Archivos agregados" -ForegroundColor Green
Write-Host ""

# Paso 5: Verificar status
Write-Host "📋 Status actual:" -ForegroundColor Yellow
git status
Write-Host ""

# Paso 6: Commit inicial
$response = Read-Host "¿Proceder con el commit inicial? (s/n)"
if ($response -eq "s" -or $response -eq "S") {
    $commitMessage = @"
🚀 Initial commit: Bus Route Manager - FastAPI + React

- Backend: FastAPI REST API with pytest, Ruff
- Frontend: React 18 + TypeScript with Vitest + Playwright
- Infrastructure: Docker + GitHub Actions CI/CD ready
- Database: PostgreSQL support
- Deployment: Railway ready
"@
    git commit -m $commitMessage
    Write-Host "✅ Commit realizado" -ForegroundColor Green
}
else {
    Write-Host "⚠️ Commit cancelado" -ForegroundColor Yellow
    exit 1
}
Write-Host ""

# Paso 7: Conectar con remote
$githubUser = Read-Host "¿Cuál es tu usuario de GitHub?"
$repoUrl = "https://github.com/$githubUser/bus-route-manager.git"

Write-Host "🔗 Agregando remote: $repoUrl" -ForegroundColor Yellow
try {
    git remote add origin $repoUrl
}
catch {
    git remote set-url origin $repoUrl
}
git remote -v
Write-Host "✅ Remote configurado" -ForegroundColor Green
Write-Host ""

# Paso 8: Push
Write-Host "📤 Subiendo a GitHub..." -ForegroundColor Yellow
Write-Host "Nota: Si es la primera vez, se te pedirá autenticación" -ForegroundColor DarkYellow
git push -u origin main

Write-Host "✅ ¡Proyecto subido a GitHub!" -ForegroundColor Green
Write-Host ""

# Paso 9: Verificar
Write-Host "🔍 Verificando..." -ForegroundColor Yellow
git log --oneline -n 3
Write-Host ""

Write-Host "═════════════════════════════════════════" -ForegroundColor Green
Write-Host "✅ Setup completado exitosamente!" -ForegroundColor Green
Write-Host "═════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "📖 Próximos pasos:" -ForegroundColor Yellow
Write-Host "1. Accede a GitHub: https://github.com/$githubUser/bus-route-manager"
Write-Host "2. Configura GitHub Secrets (Settings → Secrets)"
Write-Host "3. Lee: docs/RAILWAY_SETUP.md para configurar deployment"
Write-Host "4. Lee: docs/CICD_STRATEGY.md para entender los pipelines"
Write-Host ""
Write-Host "🎉 ¡Ahora tienes CI/CD listo con GitHub Actions!" -ForegroundColor Green
