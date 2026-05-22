from fastapi import FastAPI
from app.api.v1.endpoints.cv import router as cv_router

app = FastAPI(title="Relevo AI CV Analyzer", version="1.0.0")

# Registrar routers de la versión 1 de la API
app.include_router(cv_router, prefix="/api/v1")

# ─── Health check ────────────────────────────────────────────
# Usado por Docker Compose para verificar que el servicio está listo
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

