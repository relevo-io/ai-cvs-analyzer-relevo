import sys
import os

# Añadir el directorio actual a sys.path para poder importar config y services
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.gemini_service import analyze_cv_text

def test_analysis():
    mock_cv = """
    Pol Puig
    Desarrollador Full Stack con 5 años de experiencia.
    Educación: Grado en Ingeniería Informática.
    Habilidades: React, Node.js, TypeScript, Python, Docker, MongoDB.
    Experiencia:
    - Tech Lead en Startup Innovadora (2023 - Presente): Lideré un equipo de 4 desarrolladores.
    - Desarrollador Backend en Empresa Corp (2021 - 2023): Diseñé APIs robustas usando Express y NestJS.
    """
    
    print("Iniciando prueba de análisis de CV con Gemini...")
    try:
        result = analyze_cv_text(mock_cv)
        print("¡Prueba completada con éxito!")
        print("Resultado devuelto:")
        import pprint
        pprint.pprint(result)
    except Exception as e:
        print(f"Error durante el análisis: {e}")

if __name__ == "__main__":
    test_analysis()
