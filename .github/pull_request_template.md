## 📋 Descripción
<!-- Explica brevemente qué hace este PR y por qué es necesario -->

## 🌿 Tipo de cambio
<!-- Marca con una X la que corresponda -->
- [ ] `feature/*` → nueva funcionalidad
- [ ] `bugfix/*` → corrección de error
- [ ] `refactor/*` → mejora de código sin cambiar comportamiento
- [ ] `release/*` → preparación de release
- [ ] `hotfix/*` → fix crítico en producción

## ✅ Checklist
<!-- Completa antes de solicitar revisión -->
- [ ] El nombre de la rama sigue la convención (`feature/`, `bugfix/`, `refactor/`, `release/`, `hotfix/`)
- [ ] El PR apunta a la rama correcta (ver tabla abajo)
- [ ] Los tests pasan localmente
- [ ] Se agregaron o actualizaron tests para los cambios
- [ ] El código cumple con el estilo del proyecto (ruff / eslint sin errores)
- [ ] La documentación fue actualizada (si aplica)

## 🗺️ Estrategia de ramas
```
main
└── develop
    ├── feature/*     →  merge a develop
    ├── bugfix/*      →  merge a develop
    └── refactor/*   →  merge a develop

release/*             →  merge a main
hotfix/*              →  merge a main
```

## 🔗 Issue relacionado
<!-- Referencia el issue: "Closes #123" o "Ref #123" -->

## 📸 Evidencia (opcional)
<!-- Screenshots, videos o logs relevantes -->
