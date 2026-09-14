from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import httpx
import os
from urllib.parse import quote

# =========================
# ENVIRONMENT
# =========================
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_API_URL = os.getenv(
    "GROQ_API_URL",
    "https://api.groq.com/openai/v1/chat/completions"
)

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.1-8b-instant"
)

TIKTOK_API_URL_1 = os.getenv(
    "TIKTOK_API_URL_1",
    "https://www.tikwm.com/api"
)

TIKTOK_API_URL_2 = os.getenv(
    "TIKTOK_API_URL_2",
    "https://api.tikmate.cc/api"
)


# =========================
# APP
# =========================
app = FastAPI(
    title="WaterTik API",
    version="1.0.0"
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
        timeout = httpx.Timeout(30.0)

        async with httpx.AsyncClient(
            timeout=timeout
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
# TIKTOK ENDPOINT
# =========================
@app.get("/api/tiktok")
async def tiktok_download(url: str):

    if not url.strip():
        return {
            "status": "error",
            "message": "URL TikTok tidak boleh kosong."
        }

    encoded_url = quote(
        url.strip(),
        safe=""
    )

    tiktok_api_urls = [
        TIKTOK_API_URL_1,
        TIKTOK_API_URL_2
    ]

    async with httpx.AsyncClient(
        timeout=30.0
    ) as client:

        for api_url in tiktok_api_urls:

            try:
                response = await client.get(
                    f"{api_url}?url={encoded_url}"
                )

                if response.status_code != 200:
                    continue

                data = response.json()

                if (
                    data.get("code") == 0
                    and data.get("data")
                ):
                    return {
                        "status": "success",
                        "data": data
                    }

            except Exception:
                continue

    return {
        "status": "error",
        "message": "Kedua API TikTok gagal."
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
        "status": "ok"
    }
