import os
import pytz
import json
from datetime import datetime
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv

from utils.director import get_ai_vibe
from utils.weather import fetch_london_weather
from utils.spotify import play_vibe
from utils.led_sim import hsv_to_rgb_normalized
from utils.hardware import update_physical_led

load_dotenv()

DEFAULT_VIBE = {
    "vibe_name": "April Evening Whisper",
    "reason": "This captures the cool, cloudy, relaxed weekend evening atmosphere in London, promoting quiet introspection.",
    "spotify_search_terms": "Ambient Chill Lofi", # 万が一のために検索ワードも設定
    "hue": 9500,
    "saturation": 100,
    "brightness": 120
}

app = Flask(__name__)
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID") or os.getenv("SPOTIFY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET") or os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI") or os.getenv("SPOTIFY_REDIRECT_URI")

# --- Helper Functions ---
def load_modes():
    """Load custom lighting modes from modes.json"""
    modes_path = os.path.join(os.path.dirname(__file__), 'modes.json')
    try:
        with open(modes_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("custom_modes", []) 
    except Exception as e:
        print(f"JSON Load Error: {e}")
        return []

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get_modes')
def get_modes_api():
    """Returns all available modes to the frontend"""
    modes = load_modes()
    return jsonify({"custom_modes": modes})

@app.route('/api/update_vibe')
def update_vibe():
    # 1. Initialize default values to ensure light turns on even if AI fails
    r, g, b = 255, 100, 20  # Warm Orange
    vibe_name = "Aimos Default"
    spotify_query = "London Chill"
    spotify_info = {"status": "skipped"}

    try:
        london_tz = pytz.timezone('Europe/London')
        now_london = datetime.now(london_tz)

        time_context = {
            "full_date_time": now_london.strftime("%Y-%m-%d %H:%M:%S"),
            "hour": now_london.hour,
            "period": "Morning" if 5 <= now_london.hour < 12 else 
                      "Afternoon" if 12 <= now_london.hour < 18 else 
                      "Evening" if 18 <= now_london.hour < 22 else "Night",
            "is_weekend": now_london.weekday() >= 5
        }

        # Fetch weather data (fallback to default if API fails)
        weather_info = fetch_london_weather(OPENWEATHER_API_KEY)
        if not weather_info:
            weather_info = {"status": "Clear", "temp": 15}

        # 2. Try to get AI-generated Vibe
        try:
            vibe = get_ai_vibe(
                weather_status=weather_info.get("status", "Clear"), 
                temp=weather_info.get("temp", 15), 
                time_info=time_context  
            )

        except Exception as ai_e:
            print(f"⚠️ AI error - Falling back to default vibe: {ai_e}")
            vibe = DEFAULT_VIBE

        print("\n" + "="*50)
        print("🧠 [Aimos AI Thinking]")
        print(f"📍 Vibe Name : {vibe.get('vibe_name')}")
        print(f"💬 Reason    : {vibe.get('reason')}")
        print(f"🎵 Search For: {vibe.get('spotify_search_terms')}")
        print(f"🎨 Color     : Hue:{vibe.get('hue')}, Sat:{vibe.get('saturation')}, Bri:{vibe.get('brightness')}")
        print("="*50 + "\n")

        vibe_name = vibe.get("vibe_name", vibe_name)
        spotify_query = vibe.get("spotify_search_terms", spotify_query)
        h, s, v = vibe.get("hue", 0), vibe.get("saturation", 0), vibe.get("brightness", 0.5)
        r, g, b = hsv_to_rgb_normalized(h, s, v)


        # 3. Update hardware LEDs (Executed regardless of AI success)
        update_physical_led(r, g, b)

        # 4. Trigger Spotify playback (Safe handling for non-iterable return)
        try:
            spotify_result = play_vibe(
                spotify_query, 
                SPOTIPY_CLIENT_ID, 
                SPOTIPY_CLIENT_SECRET, 
                SPOTIPY_REDIRECT_URI
            )
            
            # If play_vibe returned a tuple (success, info), take only the info
            if isinstance(spotify_result, tuple):
                _, spotify_info = spotify_result  # _ は「使わない変数」という慣習的な書き方です
            else:
                spotify_info = {"status": "No device found"}
                
        except Exception as sp_e:
            print(f"Spotify skipped: {sp_e}")
            spotify_info = {"status": "Error"}

        return jsonify({
            "status": "success",
            "vibe_name": vibe_name,
            "rgb": [r, g, b],
            "spotify": spotify_info
        })

    except Exception as e:
        # Emergency fallback: set light to Red and log critical error
        update_physical_led(255, 0, 0)
        print(f"Critical error during update: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/play_mode/<mode_id>')
def play_mode(mode_id):
    modes = load_modes()
    mode = next((m for m in modes if m["id"] == mode_id), None)

    if not mode:
        return jsonify({"error": "Mode not found"}), 404
    
    if mode.get('is_ai'):
        return update_vibe() 
    
    # Custom Mode Logic: Set color first, then try Spotify
    r, g, b = mode['rgb']
    update_physical_led(r, g, b)

    spotify_info = {"status": "skipped"}
    try:
        spotify_result = play_vibe(
            mode["spotify_query"], 
            SPOTIPY_CLIENT_ID, 
            SPOTIPY_CLIENT_SECRET, 
            SPOTIPY_REDIRECT_URI
        )
        if isinstance(spotify_result, tuple):
            success, spotify_info = spotify_result
    except Exception as sp_e:
        print(f"Spotify skipped in custom mode: {sp_e}")

    return jsonify({
        "status": "success",
        "vibe_name": mode["name"],
        "rgb": [r, g, b],
        "spotify": spotify_info
    })

@app.route('/api/stop_vibe')
def stop_vibe():
    """Stops the current Spotify playback and turns off the LEDs"""
    try:
       # 1. Turn off the physical LEDs (RGB: 0, 0, 0)
       update_physical_led(0, 0, 0)

       # 2. Stop Spotify playback
       from utils.spotify import stop_spotify
       success = stop_spotify(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)
       
       return jsonify({
           "status": "success" if success else "error",
           "message": "Lights turned off and music stopped"
       })
    except Exception as e:
        print(f"Error during stop_vibe: {e}")
        return jsonify({"status": "error"}), 500  

if __name__ == '__main__':
    # Run server on local network
    app.run(host='0.0.0.0', port=5001, debug=True)