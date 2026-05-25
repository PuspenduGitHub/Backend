import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

HF_TOKEN = "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"

API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom-560m"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

class SoilInput(BaseModel):
    moisture: int
    ph: float
    nitrogen: str
    phosphorus: str
    potassium: str
    temperature: int


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

    Give output:
    SOIL ANALYSIS:
    FERTILIZER:
    IRRIGATION:
    CROPS:
    """

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": prompt},
            timeout=30
        )

        print("STATUS:", response.status_code)
        print("TEXT:", response.text)

        result = response.json()

        # 🔴 model loading case
        if isinstance(result, dict) and "error" in result:
            return {"report": "Model is loading... try again in 10 seconds"}

        output = result[0]["generated_text"]

        return {"report": output}

    except Exception as e:
        return {"report": f"Server error: {str(e)}"}
