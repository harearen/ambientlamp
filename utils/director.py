import json
import os
from google.genai import Client

def get_ai_vibe(weather_status, temp, time_info):
    api_key = os.getenv("GEMINI_API_KEY")
    client = Client(api_key=api_key)
    
    prompt = f"""
    Current context in London:
    - Time: {time_info['full_date_time']} ({time_info['period']})
    - Weather: {weather_status}
    - Temperature: {temp}°C
    - Weekend: {"Yes" if time_info['is_weekend'] else "No"}

    Based on the above, act as a creative director for a "Space Engine" ambient lamp.
    The lamp has a stone base and a clear sphere. Suggest a vibe that matches the 
    specific atmosphere of London right now.

    Return ONLY a JSON object:
    - "vibe_name": A creative name (e.g., "Midnight Soho Rain", "Sunday Roast Glow").
    - "spotify_query": A specific search term for a matching Spotify playlist.
    - "reason": Why this matches the current London vibe (short sentence).
    - "hue": 0-65535 (Color)
    - "saturation": 0-255 (Vividness)
    - "brightness": 0-255 (Intensity)
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt,
            config={'response_mime_type': 'application/json'}
        )
        
        vibe_data = json.loads(response.text)
        return vibe_data

    except Exception as e:
        print(f"Gemini API or Parse Error: {e}")
        return {
            "vibe_name": "London Default",
            "spotify_query": "London Lo-fi",
            "reason": "Something went wrong, but keep the vibe going.",
            "hue": 40000,
            "saturation": 100,
            "brightness": 150
        }