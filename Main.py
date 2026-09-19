from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import httpx
import os

# =========================
# ENVIRONMENT
# =========================
load_dotenv()

# ---------- GROQ ----------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_API_URL = os.getenv(
    "GROQ_API_URL",
    "https://api.groq.com/openai/v1/chat/completions"
)

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.1-8b-instant"
)

# ---------- RAPIDAPI ----------
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "")
RAPIDAPI_URL = os.getenv("RAPIDAPI_URL", "")
RAPIDAPI_PARAM = os.getenv("RAPIDAPI_PARAM", "url")


# =========================
# APP
# =========================
app = FastAPI(
    title="WaterTik API",
    version="2.0.0"
)


# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# REQUEST MODEL
# =========================
class AIRequest(BaseModel):
    question: str
    system_prompt: str | None = None


# =========================
# AI ENDPOINT
# =========================
@app.post("/api/ask-ai")
async def ask_ai(data: AIRequest):

    if not GROQ_API_KEY:
        return {
            "status": "error",
            "message": "GROQ_API_KEY tidak ditemukan di environment."
        }

    question = data.question.strip()

    if not question:
        return {
            "status": "error",
            "message": "Pertanyaan tidak boleh kosong."
        }

    system_prompt = (
        data.system_prompt
        or "Kamu adalah WaterTik AI Assistant. "
           "Jawab dengan Bahasa Indonesia yang santai, "
           "jelas, dan membantu."
    )

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": question
            }
        ],
        "temperature": 0.8,
        "max_tokens": 800,
        "stream": False
    }

    try:
        async with httpx.AsyncClient(
            timeout=30.0
        ) as client:

            response = await client.post(
                GROQ_API_URL,
                headers=headers,
                json=payload
            )

        if response.status_code != 200:

            try:
                error_data = response.json()
            except Exception:
                error_data = {}

            return {
                "status": "error",
                "message": "Request ke Groq gagal.",
                "code": response.status_code,
                "detail": error_data.get("error", {})
            }

        result = response.json()

        choices = result.get("choices", [])

        if not choices:
            return {
                "status": "error",
                "message": "Groq tidak mengembalikan jawaban."
            }

        ai_response = (
            choices[0]
            .get("message", {})
            .get("content", "")
        )

        return {
            "status": "success",
            "response": ai_response
        }

    except httpx.TimeoutException:
        return {
            "status": "error",
            "message": "Request AI timeout."
        }

    except httpx.HTTPError as e:
        return {
            "status": "error",
            "message": f"HTTP error: {str(e)}"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Server error: {str(e)}"
        }


# =========================
# TIKTOK RAPIDAPI
# =========================
@app.get("/api/tiktok")
async def tiktok_download(url: str):

    if not url.strip():
        return {
            "status": "error",
            "message": "URL TikTok tidak boleh kosong."
        }

    if not RAPIDAPI_KEY:
        return {
            "status": "error",
            "message": "RAPIDAPI_KEY belum diset."
        }

    if not RAPIDAPI_HOST:
        return {
            "status": "error",
            "message": "RAPIDAPI_HOST belum diset."
        }

    if not RAPIDAPI_URL:
        return {
            "status": "error",
            "message": "RAPIDAPI_URL belum diset."
        }

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    params = {
        RAPIDAPI_PARAM: url.strip()
    }

    try:
        async with httpx.AsyncClient(
            timeout=30.0
        ) as client:

            response = await client.get(
                RAPIDAPI_URL,
                headers=headers,
                params=params
            )

        try:
            data = response.json()
        except Exception:
            data = {}

        if response.status_code != 200:
            return {
                "status": "error",
                "message": "RapidAPI gagal.",
                "code": response.status_code,
                "detail": data
            }

        return {
            "status": "success",
            "data": data
        }

    except httpx.TimeoutException:
        return {
            "status": "error",
            "message": "RapidAPI timeout."
        }

    except httpx.HTTPError as e:
        return {
            "status": "error",
            "message": f"RapidAPI HTTP error: {str(e)}"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Server error: {str(e)}"
        }


# =========================
# ROOT
# =========================
@app.get("/")
async def read_root():

    return {
        "status": "success",
        "message": "WaterTik API is running!"
    }


# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
async def health():

    return {
        "status": "ok",
        "groq": bool(GROQ_API_KEY),
        "rapidapi": bool(RAPIDAPI_KEY)
    }
