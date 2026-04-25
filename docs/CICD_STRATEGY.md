# 🚀 CI/CD Strategy - Bus Route Manager

**Fecha**: Abril 2026  
**Versión**: 1.0  
**Audience**: 4 desarrolladores DevOps/QA

---

## 📋 Tabla de Contenidos

1. [Overview](#overview)
2. [Arquitectura](#arquitectura)
3. [Branching Strategy](#branching-strategy)
4. [Pipelines](#pipelines)
5. [Deployment Environments](#deployment-environments)
6. [Security](#security)
7. [Monitoring](#monitoring)
8. [Disaster Recovery](#disaster-recovery)

---

## 🎯 Overview

### Objetivos
- ✅ **Automatizar** build, test y deploy
- ✅ **Reducir** tiempo de release (target: <30 min)
- ✅ **Mejorar** calidad de código (coverage >75%)
- ✅ **Minimizar** costos (target: <$15/mes)
- ✅ **Garantizar** uptime >99% en producción

### Stack Elegido
```
├── VCS:          GitHub
├── CI/CD:        GitHub Actions (gratuito)
├── Registry:     GitHub Container Registry (ghcr.io)
├── Cloud:        Railway + Render (free tier optimizado)
├── Database:     PostgreSQL (Railway free)
└── Monitoring:   Prometheus/Grafana (opensource)
```

### Costo Mensual Estimado
```
GitHub Actions:      $0    (2000 min/mes free)
Railway/Render:      $0-$5 (free tier + créditos)
Database:            $0    (free tier Railway)
Domains:             $0-$12 (si usas custom domain)
─────────────────────────────
TOTAL MENSUAL:       $0-$17
```

---

## 🏗️ Arquitectura

### Flujo General

```
Developer Push
    │
    ├─→ [CI Pipeline]
    │   ├─ Lint & Format
    │   ├─ Run Tests (unit + e2e)
    │   ├─ SAST Security Scan
    │   ├─ Dependency Check
    │   └─ Docker Build Validation
    │
    └─→ [PR Review]
        └─ 2 Approvals Required
            │
            └─→ [Merge to main]
                │
                ├─→ [Dev Auto-Deploy]
                │   ├─ Build Docker images
                │   ├─ Push to ghcr.io
                │   ├─ Deploy to Railway DEV
                │   └─ Run smoke tests
                │
                └─→ [Staging Manual Deploy]
                    └─ QA Team triggers
                        │
                        └─→ [Prod Manual Deploy]
                            └─ Product Owner triggers
                                └─ Canary Deployment
                                   ├─ 5% traffic (5 min)
                                   ├─ 50% traffic (5 min)
                                   └─ 100% traffic
```

---

## 🌿 Branching Strategy

### GitFlow Simplificado

```
main (producción)
├── Tags: v1.0.0, v1.1.0, ...
├── Protection Rules:
│   ├─ Require 2 approvals
│   ├─ Dismiss stale reviews
│   ├─ Require CI to pass
│   └─ No force push
└──

develop (integración)
├── Feature branches
├── Auto-deploy to Railway DEV
└── Base para nuevas features

├─ feature/add-notifications
├─ feature/map-optimization
├─ bugfix/route-not-found
├─ chore/update-deps
└─ hotfix/critical-bug
```

### Convención de Nombres

```
feature/<feature-name>       # Nueva feature
bugfix/<bug-id>             # Bug fix
hotfix/<issue-id>           # Bugfix crítico en prod
chore/<task>                # Mantenimiento
docs/<doc-name>             # Documentación

Ejemplos:
✅ feature/real-time-tracking
✅ bugfix/GPS-accuracy-issue
✅ hotfix/database-connection-leak
✅ chore/upgrade-fastapi
```

### Workflow Diario (Para 4 Devs)

```
1. Developer A crea feature/nueva-funcionalidad
   └─ git checkout -b feature/nueva-funcionalidad

2. Commits y push
   └─ git push origin feature/nueva-funcionalidad

3. CI Pipeline corre automáticamente
   └─ Tests, linting, security scan

4. Abre Pull Request
   └─ GitHub automáticamente pide reviews

5. Developer B + C revisan (2 approvals)
   └─ Comentarios, sugerencias

6. Merge a develop
   └─ Railway DEV se actualiza automáticamente

7. QA team prueba en DEV
   └─ Si todo OK → aprobación para staging

8. Deployment a Staging
   └─ Workflow manual: "Deploy to Production"
      └─ Seleccionar "staging" en el input

9. Más QA testing
   └─ Performance, E2E, regresión

10. Deployment a Prod (Canary)
    └─ Workflow manual: "Deploy to Production"
       └─ Seleccionar "production" en el input
```

---

## 🔄 Pipelines

### 1. CI Pipeline (`ci.yml`)

**Trigger**: Pull Request, Push to main/develop

**Jobs**:

#### Backend Tests
- ✅ Linting con Ruff
- ✅ Type checking con mypy
- ✅ Pytest con cobertura
- ✅ Coverage report a Codecov

#### Frontend Tests
- ✅ Linting con ESLint
- ✅ Type checking con TypeScript
- ✅ Vitest unitarios con cobertura
- ✅ Playwright E2E (críticos)

#### Security Scan
- ✅ Trivy filesystem scan (SAST)
- ✅ Dependencia vulnerability check
- ✅ Secret scanning

#### Docker Build
- ✅ Build backend Dockerfile (no push)
- ✅ Build frontend Dockerfile (no push)

**Status Check**:
```
✅ Backend tests PASSED
✅ Frontend tests PASSED
✅ Security scan PASSED
✅ Docker build OK
└─ Ready to merge
```

### 2. Dev Deploy Pipeline (`deploy-dev.yml`)

**Trigger**: Push to main

**Duración**: ~5-10 minutos

**Steps**:
1. Build Docker images
2. Push a GitHub Container Registry
3. Deploy backend a Railway DEV
4. Deploy frontend a Railway DEV
5. Run health check
6. Notificar status

**Automático**: No requiere intervención manual

### 3. Prod Deploy Pipeline (`deploy-prod.yml`)

**Trigger**: Manual workflow dispatch

**Duración**: ~15-20 minutos

**Inputs Requeridos**:
- Version: `1.0.0` (semver)
- Environment: `staging` o `production`

**Strategy**:
```
Staging:
  1. Build imágenes
  2. Deploy a Railway Staging
  3. Health checks
  4. Create Git tag

Production (Canary):
  1. Build imágenes
  2. Deploy backend (5% traffic)
  3. Monitor 5 min
  4. Aumentar a 50%
  5. Monitor 5 min
  6. Aumentar a 100%
  7. Deploy frontend
  8. Final health check
  9. Create GitHub Release
```

---

## 🌍 Deployment Environments

### Development (Railway Free)

```
URL:            https://bus-api-dev.railway.app
Frontend:       https://bus-web-dev.railway.app
Database:       PostgreSQL free (5MB limit)
Auto-updates:   En cada push a main
Uptime SLA:     Ninguno (dev)
```

**Recursos**:
- Backend: 512MB RAM
- Frontend: 512MB RAM
- Database: PostgreSQL shared

**Para actualizar manualmente**:
```bash
cd fastapi_backend
railway link <service-id>
railway up

cd ../frontend
railway link <service-id>
railway up
```

### Staging (Railway Business o Render)

```
URL:            https://bus-api-staging.railway.app
Database:       PostgreSQL dedicated
Auto-updates:   No (manual)
Uptime SLA:     99% (best effort)
Acceso:         Solo QA team
```

**Para deployar**:
```bash
# Vía GitHub Actions
1. Click "Actions" en GitHub
2. "Deploy to Production"
3. Version: 1.0.1
4. Environment: staging
5. Run workflow
```

### Production (Railway Premium o Render)

```
URL:            https://bus-api.example.com
Frontend:       https://bus.example.com
Database:       PostgreSQL dedicated + backups
Auto-updates:   No (manual, canary)
Uptime SLA:     99.5% (best effort)
Acceso:         Solo product owner
Monitoreo:      24/7 alertas
```

**Para deployar**:
```bash
# Vía GitHub Actions (SOLO product owner)
1. Click "Actions" en GitHub
2. "Deploy to Production"
3. Version: 1.0.1
4. Environment: production
5. ✅ Requiere approval de environment
6. Run workflow
```

---

## 🔐 Security

### Secretos Requeridos en GitHub

**Para CI/CD**:
```yaml
GITHUB_TOKEN:                 # Auto-generado
RAILWAY_TOKEN:                # Tu token de Railway
```

**Para Environments**:
```yaml
# DEV
DEV_API_URL:                  https://bus-api-dev.railway.app
DEV_DATABASE_URL:             postgresql://...

# STAGING
RAILWAY_STAGING_BACKEND_SERVICE_ID:    # Tu service ID
RAILWAY_STAGING_FRONTEND_SERVICE_ID:   # Tu service ID
STAGING_API_URL:              https://bus-api-staging.railway.app

# PRODUCTION
RAILWAY_PROD_BACKEND_SERVICE_ID:       # Tu service ID
RAILWAY_PROD_FRONTEND_SERVICE_ID:      # Tu service ID
PROD_API_URL:                 https://bus-api.example.com
```

### Configurar Secretos

```bash
# Vía GitHub CLI
gh secret set RAILWAY_TOKEN --body "tu-token-aqui"

# O manualmente:
# 1. GitHub Repo → Settings → Secrets
# 2. New repository secret
# 3. Name: RAILWAY_TOKEN
# 4. Value: <tu-token>
```

### Prácticas de Seguridad

✅ **DO**:
- Usar GitHub Secrets para todo
- Rotar tokens cada 90 días
- Logs sin datos sensibles
- HTTPS en todas las URLs
- Non-root user en Docker

❌ **DON'T**:
- Commitear .env files
- Hardcodear credenciales
- Usar old/weak passwords
- Permitir force push
- Ignorar security warnings

---

## 📊 Monitoring

### Logs

```
Centralizados en:
├─ GitHub Actions (build logs)
├─ Railway dashboard (application logs)
└─ Application logs → stdout (JSON structured)
```

### Métricas Clave

```
✅ Deployment Frequency:    Daily (target)
✅ Lead Time for Changes:   < 30 min
✅ Mean Time to Recovery:   < 15 min
✅ Change Failure Rate:     < 5%
✅ Code Coverage:           > 75%
✅ Test Pass Rate:          > 95%
✅ Build Success Rate:      > 98%
```

### Health Checks

```
Backend:   GET /health → 200 OK
           Response: { "status": "healthy", "timestamp": "..." }

Frontend:  GET / → 200 OK with HTML
           Checks: API reachable, maps load
```

---

## 🔄 Disaster Recovery

### Rollback Plan

**Para Dev** (automático):
```
Si tests fallan → No deployar
Si API no responde → Railway revierte automáticamente
```

**Para Staging/Prod** (manual):
```bash
# Opción 1: Revertir a versión anterior
git revert <commit-sha>
git push origin main

# Opción 2: Cambiar tag
git tag -d v1.0.1-bad
git tag v1.0.1 v1.0.0
git push origin v1.0.1 --force

# Opción 3: Manual en Railway
railway environment switch <env-name>
```

### Backup Strategy

```
Frequency:  Daily automático
Retention:  30 días
Storage:    Railway managed backups
Manual:     Exportar backup antes de deploy
```

**Exportar backup manualmente**:
```bash
railway db export
# Descarga como .sql
```

---

## 📝 Checklist Antes de Prod

- [ ] Todas las pruebas pasan
- [ ] Coverage > 75%
- [ ] Code review aprobado por 2 personas
- [ ] Staging tested completamente
- [ ] Security scan sin críticos
- [ ] Backup realizado
- [ ] Version number actualizada (semver)
- [ ] Changelog updated
- [ ] Rollback plan documentado
- [ ] Team notificado

---

## 🆘 Troubleshooting

### Tests fallan en CI pero pasan localmente

```bash
# Check environment variables
export DATABASE_URL=postgresql://...

# Run tests localmente en Docker
docker-compose -f docker-compose.yml run backend pytest

# Check Python version
python --version  # Must be 3.12
```

### Docker build falla

```bash
# Build localmente
docker build -f fastapi_backend/Dockerfile fastapi_backend/

# Check tamaño de imagen
docker images | grep bus-route-manager

# Limpiar cache
docker system prune -a
```

### Deploy a Railway falla

```bash
# Check Railway CLI
railway --version

# Link service
railway link <service-id>

# Ver logs
railway logs

# Restart service
railway restart
```

---

## 📚 Referencias

- [GitHub Actions Docs](https://docs.github.com/actions)
- [Railway Docs](https://railway.app/docs)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [GitFlow Cheatsheet](https://danielkummer.github.io/git-flow-cheatsheet/)

---

**Última actualización**: Abril 2026  
**Próxima review**: Trimestral
