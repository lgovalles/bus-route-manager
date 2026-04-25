# ✅ CHECKLIST: Bus Route Manager - Subir a GitHub e Implementar CI/CD

**Objetivo**: Configurar el proyecto 100% ready para CI/CD en 15 minutos

---

## 🎯 Fase 1: Subir a GitHub (5 min)

### Pre-requisitos
- [ ] Tienes cuenta GitHub
- [ ] Git instalado en tu máquina
- [ ] Estás en la carpeta: `c:\Users\lovalles\bus-route-manager`

### Comandos (Ejecuta en PowerShell)

```powershell
# 1. Configura git globalmente
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@github.com"

# 2. Inicializa repositorio
cd c:\Users\lovalles\bus-route-manager
git init
git add .
git commit -m "🚀 Initial commit: Bus Route Manager - FastAPI + React

- Backend: FastAPI REST API
- Frontend: React 18 + TypeScript  
- Infrastructure: Docker + GitHub Actions ready"

# 3. Agrega remoto (REEMPLAZA TU_USUARIO)
git branch -M main
git remote add origin https://github.com/TU_USUARIO/bus-route-manager.git

# 4. Pushea a GitHub
git push -u origin main
```

### Verificar
- [ ] Accede a https://github.com/TU_USUARIO/bus-route-manager
- [ ] Ves todos tus archivos en GitHub ✅

---

## 🔒 Fase 2: Configurar GitHub Secrets (5 min)

Necesitas secretos para que los workflows puedan deployar.

### Via GitHub UI (Manual)

1. Accede a: `https://github.com/TU_USUARIO/bus-route-manager/settings/secrets/actions`
2. Click "New repository secret"
3. Agrega estos inicialmente:

```yaml
RAILWAY_TOKEN:  
  Value: Tu token de Railway (desde https://railway.app/account/tokens)

DEV_API_URL:    
  Value: (Lo sabrás después de configurar Railway)

RAILWAY_BACKEND_SERVICE_ID:
  Value: (Lo sabrás después de crear servicio en Railway)

RAILWAY_FRONTEND_SERVICE_ID:
  Value: (Lo sabrás después de crear servicio en Railway)
```

### Via GitHub CLI (Automático)

```bash
# Instala gh si no lo tienes
winget install GitHub.cli

# Auténticate
gh auth login

# Configura secretos
gh secret set RAILWAY_TOKEN --body "token-aqui"
gh secret set DEV_API_URL --body "https://bus-api-dev-xxx.up.railway.app"
gh secret set RAILWAY_BACKEND_SERVICE_ID --body "service-id-aqui"
gh secret set RAILWAY_FRONTEND_SERVICE_ID --body "service-id-aqui"
```

---

## 🚂 Fase 3: Configurar Railway (5 min)

### 1. Crear Cuenta en Railway
- [ ] Accede a https://railway.app
- [ ] Click "Get Started"  
- [ ] Login con GitHub

### 2. Crear Proyecto
- [ ] Click "New Project"
- [ ] "Deploy from GitHub repo"
- [ ] Busca `bus-route-manager`
- [ ] Autoriza Railway

### 3. Agregar Servicios

#### Backend Service
- [ ] "New Service" → "Deploy from GitHub repo"
- [ ] Select Dockerfile: `fastapi_backend/Dockerfile`
- [ ] Environment variables:
  ```
  RAILWAY_PRIVATE_DOMAIN=backend
  DATABASE_URL=${{ Ref('postgres').DATABASE_URL }}
  CORS_ORIGINS=http://localhost:5173
  PORT=8000
  ```
- [ ] Deploy

#### PostgreSQL Database
- [ ] "New Service" → "Add from marketplace"
- [ ] Select "PostgreSQL"
- [ ] Deploy (variables default OK)

#### Frontend Service
- [ ] "New Service" → "Deploy from GitHub repo"
- [ ] Select Dockerfile: `frontend/Dockerfile`
- [ ] Environment variables:
  ```
  RAILWAY_PRIVATE_DOMAIN=frontend
  VITE_API_BASE_URL=http://localhost:8000
  PORT=80
  ```
- [ ] Deploy

### 4. Obtener URLs y IDs
- [ ] Copia las URLs de cada servicio (desde Railway Dashboard)
- [ ] Copia los Service IDs (desde URL: `/service/<ID>`)
- [ ] Actualiza GitHub Secrets con estos valores

---

## ✅ Fase 4: Verificar CI/CD (Final)

### Test Workflow Automation

1. **Crea una feature branch**
   ```bash
   git checkout -b feature/test-cicd
   echo "# Test" >> README.md
   git add .
   git commit -m "test: CI/CD pipeline"
   git push origin feature/test-cicd
   ```

2. **Abre Pull Request**
   - Accede a GitHub → Tu repo
   - Click "Pull requests" → "New"
   - Select tu rama vs main
   - Click "Create pull request"

3. **Observa CI Pipeline**
   - Click en tu PR
   - Desplázate a "Checks"
   - Verifica que corre: ✅ CI - Tests & Linting
   - Si todo pasa: podrás mergear

4. **Mergea PR**
   - Click "Merge pull request"
   - Esto triggeará Deploy a Dev

5. **Verifica Deploy Automático**
   - Click en "Actions"
   - Busca "Deploy to Dev Environment"
   - Verifica que corrió exitosamente
   - Visita tu URL de dev

---

## 📋 Checklist Final

**Git & GitHub**
- [ ] Proyecto subido a GitHub
- [ ] Main branch protegida
- [ ] .gitignore configurado
- [ ] README.md presente

**Workflows Configurados**
- [ ] ci.yml (tests, linting, security)
- [ ] deploy-dev.yml (auto-deploy en main)
- [ ] deploy-prod.yml (manual, con canary)

**GitHub Secrets**
- [ ] RAILWAY_TOKEN ✅
- [ ] DEV_API_URL ✅
- [ ] RAILWAY_BACKEND_SERVICE_ID ✅
- [ ] RAILWAY_FRONTEND_SERVICE_ID ✅

**Railway Configurado**
- [ ] Cuenta creada ✅
- [ ] Backend service ✅
- [ ] Frontend service ✅
- [ ] PostgreSQL ✅
- [ ] URLs y IDs en GitHub Secrets ✅

**Docker**
- [ ] Dockerfile backend optimizado ✅
- [ ] Dockerfile frontend optimizado ✅
- [ ] docker-compose.yml para dev ✅

**Testing**
- [ ] PR triggers CI pipeline ✅
- [ ] Merge a main triggers dev deploy ✅
- [ ] Dev ambiente actualiza automáticamente ✅

**Documentation**
- [ ] docs/CICD_STRATEGY.md ✅
- [ ] docs/RAILWAY_SETUP.md ✅
- [ ] ROOT README.md ✅

---

## 🚀 Próximos Pasos (Después del Setup)

1. **Day 1**: Los 4 devs empiezan a usar el flujo
   - Branch por feature
   - PR con 2 aprobaciones
   - Auto-merge y deploy

2. **Week 1**: Optimizar pipelines
   - Reducir tiempo de tests
   - Agregar más security checks
   - Mejorar logging

3. **Week 2**: Preparar Staging/Prod
   - Crear ambiente staging en Railway
   - Configurar custom domain
   - Setup monitoreo

4. **Week 3**: Go Live
   - Deploy a producción con canary
   - Monitoring 24/7
   - Runbooks para incidents

---

## 📞 Troubleshooting Rápido

### "Los workflows no corren"
→ Verificar GitHub Secrets está correcto
→ Verificar .github/workflows/*.yml es válido YAML

### "Deploy a dev falla"
→ Ver logs en Railway Dashboard
→ Verificar DATABASE_URL es correcto
→ Verificar CORS_ORIGINS incluye frontend URL

### "Tests fallan en CI pero pasan localmente"
→ Diferencia de versiones Python/Node
→ Diferentes variables de entorno
→ Ejecutar tests en Docker: `docker-compose up -d && docker-compose run backend pytest`

### "CORS errors en frontend"
→ Backend CORS_ORIGINS no incluye frontend URL
→ Frontend VITE_API_BASE_URL incorrecto
→ Problemas de certificado SSL/HTTPS

---

## 🎓 Recursos

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Railway Docs](https://railway.app/docs)
- [Docker Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [CI/CD Best Practices](https://12factor.net/)

---

## ✨ Success Criteria

Cuando haya éxito, podrás:

✅ Hacer `git push` → tests corren automáticamente  
✅ Abrir PR → CI pipeline valida  
✅ Mergear → Deploy automático a dev  
✅ Trigger manual → Deploy a prod con canary  
✅ Ver logs → Estructura centralizada  
✅ Rollback fácil → En 1 comando  

**Tiempo total esperado**: ~15 minutos si ya tienes Railway token  
**Costo mensual**: $0-$20 (gratuito para 4 devs)  
**Escalabilidad**: Hasta 1000+ usuarios sin cambios

---

**Última actualización**: Abril 2026  
**Status**: Ready for implementation ✅
