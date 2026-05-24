from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENROUTER_API_KEY = "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"

class SoilInput(BaseModel):
    moisture: int
    ph: float
    nitrogen: str
    phosphorus: str
    potassium: str
    temperature: int

@app.get("/")
def home():
    return {"message": "API is working"}

@app.post("/analyze")
def analyze_soil(data: SoilInput):

    prompt = f"""
    Analyze this soil data:

    Moisture: {data.moisture}%
    pH: {data.ph}
    Nitrogen: {data.nitrogen}
    Phosphorus: {data.phosphorus}
    Potassium: {data.potassium}
    Temperature: {data.temperature}°C

    Give output in this format:

    SOIL ANALYSIS:
    FERTILIZER RECOMMENDATION:
    IRRIGATION ADVICE:
    SUITABLE CROPS:
    """

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistralai/mixtral-8x7b",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    result = response.json()

    if "choices" in result:
        return {"report": result["choices"][0]["message"]["content"]}
    else:
        return {"report": str(result)}
