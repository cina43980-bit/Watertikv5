import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from dotenv import load_dotenv

# Load environment variables (untuk API Key)
load_dotenv()

app = FastAPI()

# --- KONFIGURASI RAHASIA ---
# Jangan pernah tulis API Key langsung di kode ini!
# Nanti API Key dimasukkan lewat dashboard hosting (Render/Vercel/Railway)
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY") 
CEREBRAS_API_URL = "https://api.cerebras.ai/v1/chat/completions"
CEREBRAS_MODEL = "llama3.1-8b" # Bisa ganti model sesuai akun kamu

# --- SETTING CORS ---
# Mengizinkan HTML di GitHub Pages untuk akses API ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Di production, ganti * dengan URL GitHub Pages kamu
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODEL REQUEST ---
class AIRequest(BaseModel):
    question: str

# --- ENDPOINT UTAMA AI ---
@app.post("/api/ask-ai")
async def ask_ai(data: AIRequest):
    # Cek apakah API Key terisi
    if not CEREBRAS_API_KEY:
        return {
            "status": "error", 
            "message": "API Key Cerebras belum disetting di server!"
        }
    
    try:
        headers = {
            "Authorization": f"Bearer {CEREBRAS_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # System prompt ala WaterTik
        system_prompt = "Kamu adalah WaterTik AI Assistant. Jawab pertanyaan dengan Bahasa Indonesia yang santai, natural, dan ramah."
        
        payload = {
            "model": CEREBRAS_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": data.question}
            ],
            "temperature": 0.8,
            "max_tokens": 800
        }
        
        # Kirim request ke Cerebras
        response = requests.post(CEREBRAS_API_URL, headers=headers, json=payload)
        
        if response.status_code != 200:
            return {"status": "error", "message": f"Error dari Cerebras: {response.status_code}"}
            
        result = response.json()
        ai_response = result["choices"][0]["message"]["content"]
        
        return {"status": "success", "response": ai_response}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- ENDPOINT CEK SERVER (Opsional) ---
@app.get("/")
def read_root():
    return {"message": "WaterTik API is running!"}