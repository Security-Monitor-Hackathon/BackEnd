from openai import OpenAI
from google import genai
from src import config

def get_kluster_client():
    """Retorna um cliente configurado para a API da Kluster."""
    if not config.KUSTER_API_KEY:
        print("Aviso: KUSTER_API_KEY não foi configurada.")
        return None
    return OpenAI(api_key=config.KUSTER_API_KEY, base_url=config.KUSTER_BASE_URL)

def get_genai_client():
    """Retorna um cliente configurado para a API do Google GenAI."""
    if not config.GOOGLE_API_KEY:
        print("Aviso: GOOGLE_API_KEY não foi configurada.")
        return None
    # O SDK do google.generativeai configura a chave globalmente
    client = genai.Client(api_key=config.GOOGLE_API_KEY)
    return client