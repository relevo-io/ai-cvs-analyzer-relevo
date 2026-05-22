import io
import requests
from pypdf import PdfReader

def extract_text_from_url(pdf_url: str) -> str:
    response = requests.get(pdf_url)
    if response.status_code != 200:
        raise Exception(f"Error al descargar el PDF desde S3 (Status Code: {response.status_code})")
    
    # Cargar en memoria y parsear
    pdf_file = io.BytesIO(response.content)
    reader = PdfReader(pdf_file)
    
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
            
    return text
