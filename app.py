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
            API_URL,
            headers=headers,
            json={"inputs": prompt}
        )

        print("STATUS:", response.status_code)
        print("RAW:", response.text)

        result = response.json()

        if isinstance(result, dict) and "error" in result:
            return {"report": f"HF ERROR: {result['error']}"}

        if isinstance(result, list) and len(result) > 0:
            output = result[0].get("generated_text", "No output")
        else:
            output = str(result)

        return {"report": output}

    except Exception as e:
        return {"report": f"SERVER ERROR: {str(e)}"}
