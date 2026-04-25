# 🚂 Railway Setup Guide - Bus Route Manager

Este guía te ayudará a configurar Railway para hospedar gratis tu aplicación.

---

## 📋 Prerequisitos

- [ ] Cuenta GitHub (que ya tienes)
- [ ] Cuenta Railway (gratuita en https://railway.app)
- [ ] Railway CLI instalado (opcional pero recomendado)

---

## ✅ Paso 1: Crear Cuenta en Railway

1. Accede a https://railway.app
2. Click "Get Started"
3. Selecciona "Login with GitHub"
4. Autoriza Railway en GitHub

---

## ✅ Paso 2: Crear Proyecto en Railway

### Vía Railway Dashboard

1. Dentro de Railway → "New Project"
2. Selecciona "Deploy from GitHub repo"
3. Busca y selecciona `bus-route-manager`
4. Autoriza Railway para acceder a tu repo

### O vía CLI

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Crear nuevo proyecto
railway init

# Link a repositorio
railway link
```

---

## ✅ Paso 3: Configurar Servicios (Backend)

### 1. Backend Service

1. En Railway Dashboard → Tu proyecto
2. "New Service" → "Deploy from GitHub repo"
3. Selecciona `fastapi_backend/Dockerfile`
4. Variables de entorno:
   ```
   RAILWAY_PRIVATE_DOMAIN: backend
   DATABASE_URL: ${{ Ref('postgres').POSTGRES_URL }}
   CORS_ORIGINS: https://${{ Ref('frontend').RAILWAY_DOMAIN_HTTPS }}
   PORT: 8000
   ```
5. Click "Deploy"

### 2. PostgreSQL Database

1. "New Service" → "Add from marketplace"
2. Selecciona "PostgreSQL"
3. Variables por defecto están bien para dev
4. Click "Deploy"

---

## ✅ Paso 4: Configurar Frontend Service

1. "New Service" → "Deploy from GitHub repo"
2. Selecciona `frontend/Dockerfile`
3. Variables:
   ```
   RAILWAY_PRIVATE_DOMAIN: frontend
   VITE_API_BASE_URL: https://${{ Ref('backend').RAILWAY_DOMAIN_HTTPS }}
   PORT: 80
   ```
4. Click "Deploy"

---

## ✅ Paso 5: Configurar GitHub Secrets

Railway necesita ser capaz de deployar desde GitHub Actions. Configura estos secretos en GitHub:

### Obtener Railway Token

1. En Railway → "Account settings" → "Tokens"
2. Click "Create token"
3. Nombre: `GITHUB_ACTIONS_DEPLOY`
4. Copiar token

### Agregar a GitHub Secrets

```bash
gh secret set RAILWAY_TOKEN --body "token-que-copiaste"
```

O manualmente:
1. GitHub Repo → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `RAILWAY_TOKEN`
4. Value: `token-que-copiaste`

### Obtener Service IDs

En Railway Dashboard:
1. Click en cada servicio
2. En la URL verás: `railway.app/project/<PROJECT_ID>/service/<SERVICE_ID>`
3. Copia el SERVICE_ID

Agregar más secretos:

```bash
gh secret set RAILWAY_BACKEND_SERVICE_ID --body "service-id-backend"
gh secret set RAILWAY_FRONTEND_SERVICE_ID --body "service-id-frontend"
gh secret set DEV_API_URL --body "https://backend-tu-proyecto.up.railway.app"
```

---

## ✅ Paso 6: Trigger Primera Deploy

Ahora que todo está configurado, vamos a hacer el primer deploy:

```bash
# Push a main (si no lo hiciste)
git push origin main

# GitHub Actions debería ejecutar automáticamente
# Puedes ver el progreso en:
# GitHub → Actions → Deploy to Dev Environment
```

### Verificar Deploy

```bash
# En Railway Dashboard
# 1. Click en Backend → "View Logs"
# 2. Verifica que dice "Application started"
# 3. Click en "Backend Deployment" → obtén el domain
# 4. Visita https://<domain>/docs

# Test API
curl https://backend-xxx.up.railway.app/health
```

---

## 🔧 Configuración Avanzada (Opcional)

### Custom Domain

Railway permite agregar custom domain (ej: api.tudominio.com):

1. Compra dominio en Namecheap, GoDaddy, etc.
2. Railway Dashboard → Backend Service → "Domain"
3. Click "Custom Domain"
4. Ingresa `api.tudominio.com`
5. Sigue instrucciones para actualizar DNS

### Upgrade a Plan Premium

Si necesitas más recursos:

```
Railway Free:
- $5 de crédito mensual
- 512MB RAM por servicio
- Good for development

Railway Trial Pro:
- $20/mes
- 2GB RAM por servicio
- Mejor para producción
```

Para upgrade:
1. Account settings → Billing
2. Click "Upgrade"

---

## 📊 Monitoreo en Railway

### Ver Logs

```bash
# Vía CLI
railway logs --service backend

# Vía Dashboard
# Click servicio → "Logs"
```

### Métricas

En Railway Dashboard:
- CPU usage
- Memory usage
- Disk I/O
- Network I/O

### Alertas

Railway notifica automáticamente si:
- Servicio falla
- High CPU/Memory
- Deployment error

---

## 🐛 Troubleshooting

### "Build failed"

```
Problema: Dockerfile tiene error
Solución: 
- Click servicio → "Deployments"
- Click último build
- Ver logs de error
- Fix Dockerfile
- Push a GitHub → auto-redeploy
```

### "Port already in use"

```
Problema: Puerto 8000/80 ocupado
Solución:
- Railway asigna puertos automáticamente
- Verifica RAILWAY_PRIVATE_DOMAIN
```

### "Database connection failed"

```
Problema: DATABASE_URL incorrecto
Solución:
- En servicio Backend → "Variables"
- Verifica que DATABASE_URL sea correcto
- Format: postgresql://user:pass@host:5432/db
```

### "CORS errors"

```
Problema: Frontend no puede conectar con API
Solución:
- Backend → "Variables"
- Actualiza CORS_ORIGINS con URL del frontend
- Format: https://frontend-xxx.up.railway.app
- Restart servicio
```

---

## 📝 Railway Commands (CLI)

```bash
# Login
railway login

# Ver proyectos
railway projects

# Link proyecto
railway link <project-id>

# Ver servicios
railway services

# Link servicio
railway link --service <service-id>

# Ver variables
railway variables

# Set variable
railway variables set KEY=VALUE

# Unset variable
railway variables unset KEY

# Ver logs
railway logs

# Restart servicio
railway restart

# Up deploy (push cambios)
railway up

# Logout
railway logout
```

---

## 🚀 Flujo Completo: Dev → Prod

```
1. Desarrollador hace commit
   └─ git push origin feature/...

2. CI Pipeline en GitHub Actions
   └─ Tests ✅ → merge a main

3. Auto-deploy a Dev (Railway)
   └─ Backend: https://bus-backend-dev-xxx.up.railway.app
   └─ Frontend: https://bus-frontend-dev-xxx.up.railway.app

4. QA team testa en Dev
   └─ OK → Request staging deploy

5. Manual trigger staging deploy
   └─ Repo → Actions → Deploy to Production
   └─ Version: 1.0.0
   └─ Environment: staging

6. Railway deploys a staging
   └─ Otro set de contenedores en Railway
   └─ Database staging separada

7. More QA testing
   └─ Performance, E2E, etc.

8. Product Owner triggers prod deploy
   └─ Canary 5% → 50% → 100%

9. Production en Railway
   └─ https://bus-api.railway.app (custom domain)
   └─ Database con backups automáticos
```

---

## 💰 Costo Real Estimado

```
Scenario 1: 4 devs, ~150 usuarios, dev environment
──────────────────────────────────────────────────
Railway Free Tier:        $0 (5 créditos/mes)
GitHub Actions:           $0 (2000 min/mes)
Domain (opcional):        $12/año ($1/mes)
────────────────────────────────────────────────
TOTAL:                    ~$1/mes

Scenario 2: Production ready (staging + prod)
──────────────────────────────────────────────────
Railway Pro ($20/mes):    $20 (2GB RAM)
Extra services:           $5 (backups, cdn)
GitHub Actions:           $0
Domain:                   $12/año
────────────────────────────────────────────────
TOTAL:                    ~$26/mes
```

---

## 📞 Soporte

- Railway Docs: https://railway.app/docs
- GitHub Actions Docs: https://docs.github.com/actions
- Esta guía: `/docs/RAILWAY_SETUP.md`

**Última actualización**: Abril 2026
