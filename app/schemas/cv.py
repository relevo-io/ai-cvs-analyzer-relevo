from pydantic import BaseModel, Field, HttpUrl

class AnalyzeRequest(BaseModel):
    pdf_url: HttpUrl
    language: str = "es"

class CVAnalysisResponse(BaseModel):
    resumen: str = Field(description="Resumen corto del perfil profesional del candidato en 3-5 líneas")
    nota: int = Field(description="Calificación de idoneidad del candidato del 1 al 10 (un número entero de 1 a 10)")
    comentarioNota: str = Field(description="Justificación detallada de por qué se asigna esta nota")
    puntosFuertes: list[str] = Field(description="Lista de 3 a 5 habilidades o fortalezas clave detectadas")
    experienciaDestacada: list[str] = Field(description="Lista de los hitos o puestos más relevantes del historial laboral")
