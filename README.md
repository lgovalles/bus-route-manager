# 🚌 Bus Route Manager

Plataforma integral para gestión de rutas y paradas de transporte público.

## 📁 Estructura del Proyecto

```
bus-route-manager/
├── fastapi_backend/     # Backend REST API (FastAPI)
├── frontend/            # Frontend Web (React + TypeScript)
└── README.md           # Este archivo
```

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.12)
- **Database**: SQLite (desarrollo), PostgreSQL (producción)
- **Testing**: pytest
- **Code Quality**: Ruff (linter), Black (formatter)

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Testing**: Vitest (unitarios), Playwright (E2E)
- **Maps**: Leaflet

## 🚀 Quick Start

### Backend
```bash
cd fastapi_backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```
Accede a: http://localhost:8000/docs

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Accede a: http://localhost:5173

## 📋 Testing

### Backend
```bash
cd fastapi_backend
pytest                  # Ejecutar todos los tests
pytest -v              # Verbose
pytest --cov          # Con cobertura
```

### Frontend
```bash
cd frontend
npm run test           # Tests unitarios
npm run test:e2e      # Tests E2E
npm run test:coverage # Cobertura
```

## 📚 Documentation

- [Backend README](fastapi_backend/README.md)
- [Frontend README](frontend/README.md)
- [CI/CD Strategy](docs/CICD_STRATEGY.md) (próximamente)
- [Architecture](docs/ARCHITECTURE.md) (próximamente)

## 🤝 Contributing

1. Crea una rama desde `develop`: `git checkout -b feature/tu-feature`
2. Haz commit de tus cambios
3. Abre un Pull Request
4. Los tests deben pasar antes de mergear

## 📝 License

MIT License

## 👥 Team

Bus Route Manager - Public Transport Management System
