# Multi-stage build para FastAPI - Optimizado para bajo costo
FROM python:3.12-slim as builder

WORKDIR /build

# Instalar dependencies de build
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Crear wheels para instalar rápido en stage final
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements.txt

# === Final Stage ===
FROM python:3.12-slim

WORKDIR /app

# Instalar runtime dependencies solamente
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root por seguridad
RUN useradd -m -u 1000 appuser

# Copiar wheels del builder
COPY --from=builder /build/wheels /wheels
COPY --from=builder /build/requirements.txt .

# Instalar dependencias desde wheels (mucho más rápido)
RUN pip install --no-cache /wheels/*

# Copiar código de la aplicación
COPY app/ ./app
COPY seed.py .

# Cambiar propiedad de archivos
RUN chown -R appuser:appuser /app

# Cambiar a usuario no-root
USER appuser

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando de inicio
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
