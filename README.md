# Relevo IA - Servicio de Análisis de CVs

Este es el microservicio de Inteligencia Artificial de **Relevo**, desarrollado en Python utilizando **FastAPI**. Se encarga de descargar currículums en formato PDF desde buckets de Amazon S3, procesar su contenido de texto y analizarlos inteligentemente utilizando modelos de la familia **Gemini (Google AI)** para evaluar la idoneidad de los candidatos de cara a ofertas específicas.

---

## Características Principales

- **FastAPI**: Endpoints asíncronos rápidos y documentación auto-generada interactiva.
- **Integración con Gemini**: Invocación estructurada con tolerancia a fallos, recorriendo modelos prioritarios (`gemini-3.5-flash`, `gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-1.5-flash`).
- **Descarga Segura de S3**: Consumo directo en memoria de archivos PDF desde URLs pre-firmadas utilizando `pypdf`.
- **Seguridad por API Key**: Protección de endpoints mediante validación estricta de la cabecera `X-API-Key`.
- **Arquitectura de Software Profesional**: Separación limpia de responsabilidades por capas (API, Servicios, Esquemas y Configuración).
- **Dockerizado en Producción**: Dockerfile optimizado (no corre como root, variables de producción pre-configuradas y peso reducido).

---

## 📁 Estructura del Proyecto

El proyecto sigue una arquitectura modular profesional:

```text
relevo-ia-python/
├── app/
│   ├── api/                   # Controladores y Endpoints de la API
│   │   └── v1/
│   │       └── endpoints/
│   │           └── cv.py      # Ruta /api/v1/cv/analyze
│   ├── core/                  # Configuraciones globales y seguridad
│   │   ├── config.py          # Validación estricta de variables de entorno (.env)
│   │   └── security.py        # Middleware de autorización X-API-Key
│   ├── schemas/               # Esquemas Pydantic para validación y tipado
│   │   └── cv.py              # Modelos de entrada/salida y esquema JSON para Gemini
│   ├── services/              # Lógica de negocio (Capas de servicios)
│   │   ├── gemini_service.py  # Conector de IA y reintentos automáticos
│   │   └── pdf_service.py     # Descargador e intérprete de PDFs
│   └── main.py                # Entrada de la aplicación FastAPI
├── Dockerfile                 # Imagen Docker optimizada
├── .dockerignore              # Exclusiones de contexto para construcción de Docker
├── .gitignore                 # Exclusiones de Git
├── requirements.txt           # Dependencias de Python
└── test_cv_analysis.py        # Script E2E de prueba local
```

---

## 🛠️ Instalación y Configuración Local

### Prerrequisitos

- Python 3.11 o superior.
- Una clave de API de Google Gemini (`GEMINI_API_KEY`).

### Paso 1: Clonar o acceder al directorio

```bash
cd relevo-ia-python
```

### Paso 2: Crear un entorno virtual

Puedes usar Conda o el módulo `venv` estándar de Python:

**Con venv:**

```bash
python -m venv venv
source venv/bin/activate  # En macOS/Linux
# o venv\Scripts\activate en Windows
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Variables de entorno

Crea un archivo `.env` en la raíz de la carpeta `relevo-ia-python/`:

```env
GEMINI_API_KEY=tu_gemini_api_key_aqui
API_KEY=tu_token_de_seguridad_para_backend_node
```

### Paso 5: Arrancar el servidor

```bash
uvicorn app.main:app --reload --port 8000
```

El servidor estará disponible en `http://localhost:8000`. Puedes acceder a la documentación interactiva en:

- **Swagger UI:** `http://localhost:8000/docs`
- **Redoc:** `http://localhost:8000/redoc`

---

## 🐳 Despliegue con Docker

Hemos optimizado el archivo `Dockerfile` para que cumpla con los estándares más exigentes de seguridad y rendimiento. Dispones de varias opciones de despliegue:

### Opción 1: Ejecutar desde Docker Hub (Imagen de Producción)

Puedes ejecutar directamente la imagen oficial y optimizada alojada en Docker Hub:

```bash
docker run -d \
  -p 8000:8000 \
  -e GEMINI_API_KEY="tu_clave_de_gemini" \
  -e API_KEY="tu_token_de_seguridad" \
  --name relevo-ia-service \
  polp2/relevo-ia-python:latest
```

### Opción 2: Configuración en Producción con Docker Compose

Si estás integrando el microservicio en un entorno multi-contenedor orquestado por Docker Compose, puedes usar la siguiente definición:

```yaml
relevo-ia-service:
  image: polp2/relevo-ia-python:latest
  container_name: relevo-ia-service
  env_file:
    - .env
  restart: unless-stopped
  ports:
    - "8000:8000"
  networks:
    - relevo-net
  healthcheck:
    test:
      [
        "CMD",
        "python",
        "-c",
        "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')",
      ]
    interval: 30s
    timeout: 10s
    retries: 3
    start_period: 20s
```

> [!NOTE]
> Asegúrate de tener el archivo `.env` en la misma ruta con los valores para `GEMINI_API_KEY` y `API_KEY`.

### Opción 3: Construir y ejecutar la imagen localmente

Si necesitas modificar el código y reconstruir la imagen localmente:

**1. Construir la imagen:**

```bash
docker build -t relevo-ia-python .
```

**2. Arrancar el contenedor:**

```bash
docker run -d \
  -p 8000:8000 \
  -e GEMINI_API_KEY="tu_clave_de_gemini" \
  -e API_KEY="tu_token_de_seguridad" \
  --name relevo-ia-service \
  relevo-ia-python
```

---

## 🛡️ Seguridad y Endpoints

### 🔐 Autorización

Todas las rutas bajo `/api/v1` requieren el envío de la clave de acceso compartida mediante la cabecera:
`X-API-Key: <tu_token_de_seguridad>`

### 📄 Análisis de CV: `POST /api/v1/cv/analyze`

Envía la URL firmada de S3 de un currículum para que sea analizado por Gemini de acuerdo a los requerimientos de la vacante.

- **Cuerpo de la Petición (JSON):**

  ```json
  {
    "pdf_url": "https://s3.amazonaws.com/tu-bucket/cv.pdf"
  }
  ```

- **Respuesta Exitosa (JSON Estructurado):**
  ```json
  {
    "resumen": "Resumen ejecutivo del perfil del candidato...",
    "nota": 8,
    "comentarioNota": "Explicación detallada de por qué se asigna esta nota...",
    "puntosFuertes": [
      "Fuerte competencia en arquitecturas Cloud...",
      "Experiencia liderando equipos de desarrollo..."
    ],
    "experienciaDestacada": [
      "Tech Lead en Startup XYZ (2023 - Presente)",
      "Senior Full Stack Developer (2020 - 2023)"
    ]
  }
  ```
