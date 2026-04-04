import os
import json
# from google.genai import Client 

# client = Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_ai_vibe(status, temp, current_time=None): 

    # print(f"🕒 Processing vibe for London at {current_time}:00 (Weather: {status})")

    # prompt = f"""
    # Current London Weather: {status}, Temperature: {temp}°C.
    # Suggest a creative 'vibe' for my room.
    # Return ONLY a JSON object with these keys:
    # - "vibe_name": A creative name for the mood.
    # - "spotify_query": A specific search term for a Spotify playlist.
    # - "reason": Why you chose this (short sentence).
    # - "hue": A number between 0 and 65535 for a smart light.
    # - "saturation": 0-255 (Vividness: 0 is white, 255 is pure color)
    # - "brightness": 0-255 (Intensity: 0 is off, 255 is max)
    # """

    # response = client.models.generate_content(
    #     model="gemini-2.5-flash",
    #     contents=prompt,
    #     config={'response_mime_type': 'application/json'}
    # )

    # try:
    #     raw_text = response.text.strip().replace('```json', '').replace('```', '')
    #     vibe_data = json.loads(raw_text)

    #     if isinstance(vibe_data, dict) and "hue" in vibe_data:
    #         return vibe_data
    # except Exception as e:
    #     print(f"Manual Parse Error: {e}")

    # print("Using fallback vibe.")
    print("🛠️  [Dev Mode] Returning Mock Vibe Data (Token Saved)")
    return {
        "vibe_name": "Development Indigo",
        "spotify_query": "deep focus ambient",
        "reason": "Currently in development mode. Saving tokens for the big demo!",
        "hue": 43690,      # 青系の色
        "saturation": 200,
        "brightness": 150
    }