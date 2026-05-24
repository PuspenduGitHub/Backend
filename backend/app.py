import requests
import os
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

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
        }
    )

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    result = response.json()

    try:
        output = result["candidates"][0]["content"]["parts"][0]["text"]
    except:
        output = str(result)

    return {"report": output}
