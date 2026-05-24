

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# ✅ Enable CORS (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
OPENROUTER_API_KEY = os.getenv("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")

# ✅ Input model
class SoilInput(BaseModel):
    moisture: int
    ph: float
    nitrogen: str
    phosphorus: str
    potassium: str
    temperature: int


# ✅ Test route (check server working)
@app.get("/")
def home():
    return {"message": "Backend running 🚀"}


# ✅ Main AI route
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
Explain soil condition clearly.

FERTILIZER RECOMMENDATION:
List exact fertilizers.

IRRIGATION ADVICE:
Give watering advice.

SUITABLE CROPS:
Suggest crops.
"""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                # ✅ stable model (important fix)
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )

        # 🔍 Debug (check terminal)
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        if response.status_code != 200:
            return {"report": "API Error: " + response.text}

        result = response.json()

        if "choices" not in result:
            return {"report": "Invalid response: " + str(result)}

        output = result["choices"][0]["message"]["content"]

        return {"report": output}

    except Exception as e:
        return {"report": "Server Error: " + str(e)}
