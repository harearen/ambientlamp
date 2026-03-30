PRESETS = {
    "Clear": {
        "vibe_name": "Golden West End Morning", 
        "hue": 10000,       
        "color_code": "\033[38;5;220m",                    
        "playlist_id": "37i9dQZF1DX4sWypRv3w9c" 
    },
    "Clouds": {
        "vibe_name": "Moody London Afternoon",
        "hue": 100000,
        "color_code": "\033[38;5;13m",
        "playlist_id": "1ocqFRrQpH3fvsUyWJ2Kya" 
    },
    "Rain": {
        "vibe_name": "Rainy Theater District",  
        "hue": 45000,   
        "color_code": "\033[38;5;33m",                        
        "playlist_id": "37i9dQZF1DXbvABuAyZ0Yv" 
    }
}

def get_vibe(status):

    vibe = PRESETS.get(status, PRESETS["Clouds"])
    return vibe

# import os
# from genai import Client
# import json
# from dotenv import load_dotenv

# load_dotenv()

# client = Client()

# def get_ai_vibe(status, temp):
#     prompt = f"""
#     Act as a sophisticated Spatial Ambience Agent for a luxury residence in London.
#     Current conditions: Weather is {status}, Temperature is {temp}°C.

#     Task:
#     Propose a unique, poetic "Vibe" that harmonizes the indoor atmosphere with the outdoor London environment.
#     Think about how the current humidity, light quality, and chill should be balanced by light and sound.

#     Requirements:
#     1. vibe_name: A short, poetic title (English).
#     2. reason: A single, evocative sentence explaining the atmospheric intent (English).
#     3. hue: A Philips Hue compatible value (0-65535) representing the light color.
#     4. spotify_query: 3-5 specific keywords to search for a matching Spotify playlist (English).

#     Response Format:
#     Return ONLY a valid JSON object in the following format:
#     {{
#         "vibe_name": "string",
#         "reason": "string",
#         "hue": int,
#         "spotify_query": "string"
#     }}
#     """

#     try:
#         response = client.models.generate_content(
#             model="gemini-2.0-flash",
#             contents=prompt
#         )
        
#         res_text = response.text.replace('```json', '').replace('```', '').strip()
#         return json.loads(res_text)
#     except Exception as e:
#         print(f"AI generative error: {e}")
#         return {
#            "vibe_name": "Silver Silence",
#             "reason": "A minimal ambient layer to match the quiet London sky.",
#             "hue": 42000,
#             "spotify_query": "london ambient library"
#         }