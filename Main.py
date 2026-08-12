from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

# Load environment variables (dari .env atau Dashboard Koyeb/Render)
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AIRequest(BaseModel):
    question: str

@app.post("/api/ask-ai")
async def ask_ai(data: AIRequest):
    # AMBIL KEY DARI ENVIRONMENT VARIABLE
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    if not GROQ_API_KEY:
        return {"status": "error", "message": "API Key Groq tidak ditemukan di environment!"}
    
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


@app.get("/api/tiktok")
async def tiktok_download(url: str):
    TIKTOK_API_URLS = [
        "https://www.tikwm.com/api",
        "https://api.tikmate.cc/api"
    ]
    
    for api_url in TIKTOK_API_URLS:
        try:
            response = requests.get(f"{api_url}?url={url}")
            data = response.json()
            if data.get("code") == 0 and data.get("data"):
                return {"status": "success", "data": data}
        except:
            continue
            
    return {"status": "error", "message": "Kedua API TikTok gagal."}

@app.get("/")
def read_root():
    return {"message": "WaterTik API is running!"}
