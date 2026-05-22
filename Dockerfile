# Usamos la imagen oficial slim de python
FROM python:3.11-slim

# Configuraciones de entorno recomendadas para producción en Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Creamos un grupo y usuario sin privilegios para ejecutar la aplicación
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -m -s /sbin/nologin appuser

# Instalamos dependencias primero (aprovecha la caché de capas de Docker)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiamos solo el código fuente de la aplicación (excluyendo lo del .dockerignore)
COPY app/ ./app/

# Cambiamos la propiedad de la carpeta de trabajo al nuevo usuario
RUN chown -R appuser:appgroup /app

# Cambiamos al usuario sin privilegios
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
