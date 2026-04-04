import os
from dotenv import load_dotenv
# from utils.director import get_vibe
from utils.director import get_ai_vibe
from utils.weather import fetch_london_weather
from utils.spotify import play_vibe
from utils.led_sim import hsv_to_rgb_normalized


load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

def main():
    print("--- Phase 1: AI Ambient Engine ---")

    weather_info = fetch_london_weather(OPENWEATHER_API_KEY)
    status = weather_info["status"]
    temp = weather_info["temp"]
    print(f"Current London: [{status}] {temp}°C")


    if weather_info:
        current_status = weather_info["status"]
        current_temp = weather_info["temp"]
        print(f"success: current weather in London is [{current_status}], temp is [{current_temp}]")

    vibe = get_ai_vibe(status, temp)

    h=vibe.get("hue", 0)
    s=vibe.get("saturation", 0)
    v=vibe.get("brightness", 0)

    r, g, b = hsv_to_rgb_normalized(h, s, v)

    terminal_color = f"\033[38;2;{r};{g};{b}m"
    reset = "\033[0m"

    print(f"\n{terminal_color}██████████████████████████████")
    print(f"🎬 VIBE: {vibe['vibe_name']}")
    print(f"💡 LED RGB: ({r}, {g}, {b})")
    print(f"📜 REASON: {vibe['reason']}")
    print(f"██████████████████████████████{reset}\n")

    print(f"\n{terminal_color}🎬 VIBE NAME: {vibe['vibe_name']}")
    print(f"📜 INTENT: {vibe['reason']}")
    print(f"🔍 SEARCH KEYWORDS: {vibe['spotify_query']}{reset}\n")

    print("🎵 Attempting to sync with Spotify...")

    try:
        play_vibe(vibe['spotify_query'],
        SPOTIFY_CLIENT_ID,
        SPOTIFY_CLIENT_SECRET,
        SPOTIFY_REDIRECT_URI) 
    except Exception as e:
        print(f"Spotify Notice: {e}")

if __name__ == "__main__":
    main()