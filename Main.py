from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# --- SETTING CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODEL AI ---
class AIRequest(BaseModel):
    question: str

# ========================================
# ENDPOINT AI (GROQ)
# ========================================
@app.post("/api/ask-ai")
async def ask_ai(data: AIRequest):
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    if not GROQ_API_KEY:
        return {"status": "error", "message": "API Key Groq belum disetting di Render!"}
    
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "Kamu adalah WaterTik AI Assistant. Jawab dengan Bahasa Indonesia yang santai."},
                {"role": "user", "content": data.question}
            ],
            "temperature": 0.8,
            "max_tokens": 800,
            "stream": False
        }
        
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        
        if response.status_code != 200:
            return {"status": "error", "message": f"Error dari Groq: {response.status_code}"}
            
        result = response.json()
        ai_response = result["choices"][0]["message"]["content"]
        
        return {"status": "success", "response": ai_response}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ========================================
# ENDPOINT TIKTOK (Download, Generator, Slide)
# ========================================
@app.get("/api/tiktok")
async def tiktok_download(url: str):
    TIKTOK_API_URL = os.getenv("TIKTOK_API_URL")
    
    if not TIKTOK_API_URL:
        return {"status": "error", "message": "TikTok API URL belum disetting di Render!"}
    
    try:
        response = requests.get(f"{TIKTOK_API_URL}?url={url}")
        data = response.json()
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ========================================
# CEK SERVER
# ========================================
@app.get("/")
def read_root():
    return {"message": "WaterTik API is running!"}
