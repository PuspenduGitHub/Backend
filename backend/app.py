import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# ✅ Your Hugging Face Token
HF_TOKEN = "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"

# ✅ Stable model (works better than flan-t5)
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
    print("RESPONSE:", response.text)

    result = response.json()

    # ✅ Handle errors (like model loading)
    if isinstance(result, dict) and "error" in result:
        return {"report": result["error"]}

    # ✅ Extract output safely
    try:
        output = result[0]["generated_text"]
    except:
        output = str(result)

    return {"report": output}
