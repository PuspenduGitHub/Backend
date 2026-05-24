

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 IMPORTANT: get from environment
OPENROUTER_API_KEY = os.getenv("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")

class SoilInput(BaseModel):
    moisture: int
    ph: float
    nitrogen: str
    phosphorus: str
    potassium: str
    temperature: int

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/analyze")
def analyze_soil(data: SoilInput):

    if not OPENROUTER_API_KEY:
        return {"report": "ERROR: API KEY NOT FOUND"}

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
    ...

    FERTILIZER RECOMMENDATION:
    ...

    IRRIGATION ADVICE:
    ...

    SUITABLE CROPS:
    ...
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
    print(result)

    if "choices" in result:
        return {"report": result["choices"][0]["message"]["content"]}
    else:
        return {"report": str(result)}
