import json
import google.generativeai as genai
from app.core.config import settings
from app.schemas.cv import CVAnalysisResponse

# Configuración de Google Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)

def analyze_cv_text(cv_text: str, language: str = "es") -> dict:
    # Intentamos usar los modelos más recientes disponibles (gemini-3.5-flash, gemini-2.5-flash, gemini-2.0-flash, gemini-1.5-flash)
    models_to_try = ['gemini-3.5-flash', 'gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash']
    last_error = None
    
    lang_names = {
        "es": "español",
        "ca": "catalán",
        "en": "inglés"
    }
    target_lang = lang_names.get(language, "español")
    
    prompt = f"""
    Eres un consultor experto en recursos humanos y adquisición de empresas. 
    Analiza el siguiente texto extraído del currículum de un candidato interesado en adquirir o suceder un negocio.
    Extrae la información estructurada acorde a las especificaciones.
    
    IMPORTANTE: Genera todo el contenido textual del análisis (los valores de los campos 'resumen', 'comentarioNota', 'puntosFuertes' y 'experienciaDestacada') obligatoriamente en idioma {target_lang}.
    
    Texto del currículum:
    \"\"\"{cv_text}\"\"\"
    """
    
    for model_name in models_to_try:
        try:
            print(f"Intentando análisis con modelo: {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=CVAnalysisResponse
                )
            )
            return json.loads(response.text)
        except Exception as e:
            last_error = e
            print(f"Error con modelo {model_name}: {e}")
            continue
            
    raise Exception(f"Todos los modelos de Gemini fallaron. Último error: {last_error}")
