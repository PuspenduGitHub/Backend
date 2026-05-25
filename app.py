import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ⚠️ REPLACE THIS WITH NEW KEY (your current one is exposed)
OPENROUTER_API_KEY = "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"

MODEL = "meta-llama/llama-3-8b-instruct"

class SoilInput(BaseModel):
    moisture: int
    ph: float
    nitrogen: str
    phosphorus: str
    potassium: str
    temperature: int

@app.post("/analyze")
def analyze_soil(data: SoilInput):
    try:
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
                "Content-Type": "application/json",
                "HTTP-Referer": "https://your-app.onrender.com",  # ✅ REQUIRED
                "X-Title": "AgriRoverAI"  # ✅ REQUIRED
            },
            json={
                "model": MODEL,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=30
        )

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        result = response.json()

        if "error" in result:
            return {"report": f"ERROR: {result['error']['message']}"}

        output = result["choices"][0]["message"]["content"]

        return {"report": output}

    except Exception as e:
        return {"report": f"SERVER ERROR: {str(e)}"}
