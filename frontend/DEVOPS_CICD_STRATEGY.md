# Estrategia CI/CD + DevSecOps para Frontend y Backend

## 1) Estrategia de CI/CD

### Arquitectura recomendada

flowchart textual:

[Developer Push/PR]
  -> [PR Checks: lint + unit/integration tests + SAST/SCA + secret scan]
  -> [Merge to develop]
  -> [Deploy Dev automático]
  -> [Smoke tests]
  -> [Promote to staging con aprobación]
  -> [E2E + DAST]
  -> [Promote to prod con aprobación + change window]

### Entornos

- dev: despliegue automático desde develop.
- qa: validación funcional con datos controlados.
- staging: espejo de producción para pruebas finales.
- prod: despliegue progresivo con rollback automático.

### Branching strategy

- Recomendado: Trunk Based + ramas cortas.
- Ramas permanentes: main (producción), develop (integración).
- Convención: feat/, fix/, chore/, sec/.
- Pull Request obligatorio con checks verdes y al menos 1 aprobación.

### Versionado

- SemVer:
  - MAJOR: cambios incompatibles.
  - MINOR: nuevas funcionalidades compatibles.
  - PATCH: correcciones.
- Tags automáticos en release usando Conventional Commits.

## 2) Seguridad (DevSecOps)

### Controles implementados en CI

- Secret scanning: Gitleaks.
- SCA frontend: npm audit high+.
- SCA backend: pip-audit.
- SAST backend: Bandit.

### Controles recomendados siguientes

- SAST avanzado: Semgrep o CodeQL para ambos repos.
- DAST en staging: OWASP ZAP baseline.
- Firma y SBOM:
  - SBOM con Syft.
  - Firma de artefactos con Cosign.

### Gestión de secretos

- Nunca en repositorio ni variables hardcoded.
- Usar secretos del proveedor CI para corto plazo.
- Escalar a Vault / Azure Key Vault / AWS Secrets Manager para producción.

## 3) Calidad de la Aplicación

### Gates por tipo de proyecto

- Frontend:
  - npm run typecheck
  - npm run lint
  - npm run test:coverage
  - npm run build
- Backend:
  - ruff check .
  - ruff format --check .
  - pytest --cov=app --cov-fail-under=80

### Cobertura objetivo

- Inicio: 70%-80% mínimo por componente crítico.
- Objetivo trimestral: >=85% en dominio y servicios.

## 4) Buenas Prácticas de Código

- PR template obligatorio con checklist de calidad y rollback.
- Lint y format bloqueantes en CI.
- Principios:
  - SOLID en capa de dominio/servicios.
  - Clean Code en nombres, funciones pequeñas, bajo acoplamiento.
  - Clean Architecture progresiva en backend (routers -> services -> repositories).

## 5) Estructura del Proyecto

### Organización recomendada

- frontend:
  - src/components, src/pages, src/services, src/store, src/types
- fastapi_backend:
  - app/routers, app/schemas, app/models

### Evolución sugerida backend

- Agregar app/services para reglas de negocio.
- Agregar app/repositories para acceso a datos.
- Mantener routers delgados (sin lógica compleja).

### IaC

- Recomendado incorporar Terraform para:
  - ambientes dev/staging/prod
  - redes, base de datos, observabilidad, secretos

## 6) Observabilidad y Operación

### Logging, métricas y trazas

- Logging estructurado JSON (correlation id por request).
- Métricas:
  - latencia p95/p99
  - tasa de error
  - throughput
- Trazabilidad distribuida:
  - OpenTelemetry + backend tracing export.

### Alertas

- SLO sugeridos:
  - disponibilidad API >= 99.9%
  - error rate < 1%
- Alertar por:
  - incremento de 5xx
  - latencia p95 fuera de umbral
  - fallos de deploy

### Rollback y zero-downtime

- Blue/Green o Canary para prod.
- Rollback automático si smoke checks fallan.
- Migraciones de DB backward compatible.

## Herramientas recomendadas (pros y contras)

### GitHub Actions
- Pros: integración nativa con PR/checks, simple para equipos pequeños y medianos.
- Contras: complejidad crece en pipelines muy grandes sin reutilización modular.

### Ruff (backend)
- Pros: rápido, reemplaza varias herramientas de lint/format.
- Contras: menos reglas de seguridad que una suite dedicada.

### Bandit + pip-audit + npm audit
- Pros: cobertura inmediata de seguridad sin alta complejidad.
- Contras: posibles falsos positivos, requiere baseline y triage.

### Dependabot
- Pros: parches de dependencias automáticos.
- Contras: puede generar alto volumen de PR sin políticas de priorización.

## Política mínima de protección de ramas

- Branch protection en main y develop:
  - Requerir PR.
  - Requerir checks de CI exitosos.
  - Requerir 1 aprobación mínima.
  - Bloquear force push.
  - Bloquear merge con conversaciones sin resolver.

## Roadmap de adopción

- Fase 1 (actual): CI de calidad + seguridad básica + governance de PR.
- Fase 2: DAST en staging + SonarQube/CodeQL + quality gates avanzados.
- Fase 3: despliegue progresivo, observabilidad completa y SLO con alertas automáticas.
