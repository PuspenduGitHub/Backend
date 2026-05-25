import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 🔥 Paste your OpenRouter API Key here
OPENROUTER_API_KEY = "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"

# ✅ Free model (no billing needed)
MODEL = "mistralai/mistral-7b-instruct"

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
                "Content-Type": "application/json"
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

        # ✅ Handle errors
        if "error" in result:
            return {"report": f"ERROR: {result['error']['message']}"}

        output = result["choices"][0]["message"]["content"]

        return {"report": output}

    except Exception as e:
        return {"report": f"SERVER ERROR: {str(e)}"}
