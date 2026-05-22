import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Settings:
    PORT: int = int(os.getenv("PORT", 8000))
    API_KEY: str = os.getenv("API_KEY", "default_secret_key")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")

    def __init__(self):
        if not self.GEMINI_API_KEY:
            raise ValueError("Falta configurar la variable de entorno GEMINI_API_KEY")

settings = Settings()
