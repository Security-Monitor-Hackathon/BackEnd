import os
from dotenv import load_dotenv

load_dotenv()

# --- Configs do Serviço Image-to-Text (Kluster) ---
KUSTER_API_KEY = os.getenv("KUSTER_API_KEY")
KUSTER_BASE_URL = "https://api.kluster.ai/v1"
KUSTER_MODEL_NAME = "Qwen/Qwen2.5-VL-7B-Instruct"

# --- Configs do Serviço Info-Extraction (Google GenAI) ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_MODEL_NAME = "gemini-1.5-flash"