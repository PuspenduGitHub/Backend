import requests
import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# ✅ Put your Gemini API key in Render ENV
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

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

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

        response = requests.post(
            url,
            json={
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ]
            },
            timeout=30
        )

        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        result = response.json()

        # ✅ Handle Gemini errors
        if "error" in result:
            return {"report": f"ERROR: {result['error']['message']}"}

        output = result["candidates"][0]["content"]["parts"][0]["text"]

        return {"report": output}

    except Exception as e:
        return {"report": f"SERVER ERROR: {str(e)}"}
