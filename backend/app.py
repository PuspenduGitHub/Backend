import requests
import os

GEMINI_API_KEY = os.getenv("AIzaSyBnZwqMC_vysVz0BwPdEZ9GBFfFx7kt9QE")

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
    ...

    FERTILIZER RECOMMENDATION:
    ...

    IRRIGATION ADVICE:
    ...

    SUITABLE CROPS:
    ...
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

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
        }
    )

    result = response.json()
    print(result)

    try:
        output = result["candidates"][0]["content"]["parts"][0]["text"]
    except:
        output = str(result)

    return {"report": output}
