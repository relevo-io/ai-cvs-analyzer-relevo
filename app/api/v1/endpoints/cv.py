from fastapi import APIRouter, HTTPException, Security, status
from app.schemas.cv import AnalyzeRequest
from app.core.security import validate_api_key
from app.services.pdf_service import extract_text_from_url
from app.services.gemini_service import analyze_cv_text

router = APIRouter()

@router.post("/analyze", dependencies=[Security(validate_api_key)])
async def analyze_cv(payload: AnalyzeRequest):
    try:
        # 1. Extraer texto del PDF
        try:
            text = extract_text_from_url(str(payload.pdf_url))
        except Exception as download_err:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al descargar o procesar el archivo PDF: {str(download_err)}"
            )
            
        if not text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El documento PDF no contiene texto legible"
            )

        # 2. Analizar usando Gemini y retornar JSON
        analysis_result = analyze_cv_text(text, payload.language)
        return analysis_result
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en el análisis de Gemini: {str(e)}"
        )
