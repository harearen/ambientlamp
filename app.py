import os
import pytz
from datetime import datetime
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv

from utils.director import get_ai_vibe
from utils.weather import fetch_london_weather
from utils.spotify import play_vibe
from utils.led_sim import hsv_to_rgb_normalized

load_dotenv()

app = Flask(__name__)
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
SPOTIPY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/update_vibe')
def update_vibe():

    try:
        london_tz = pytz.timezone('Europe/London')
        now_london = datetime.now(london_tz)
        current_time = now_london.strftime("%Y-%m-%d %H:%M:%S")

        print(f"🕒 Updating vibe at {current_time} in London...")

        weather_info = fetch_london_weather(OPENWEATHER_API_KEY)
        if not weather_info:
            return jsonify({"error": "Failed to fetch weather data"}), 500

        vibe = get_ai_vibe(weather_info["status"], weather_info["temp"], current_time)

        success, spotify_info = play_vibe(
            vibe["spotify_query"], 
            SPOTIPY_CLIENT_ID, 
            SPOTIPY_CLIENT_SECRET, 
            SPOTIPY_REDIRECT_URI
        )

        h = vibe.get("hue", 0)
        s = vibe.get("saturation", 0)
        v = vibe.get("brightness", 0)

        r, g, b = hsv_to_rgb_normalized(h, s, v)

        
        return jsonify({
        "status": "success",
        "vibe_name": vibe["vibe_name"],
        "reason": vibe["reason"],
        "rgb": [r, g, b],
        "spotify": spotify_info,
        "spotify_status": "success" if success else "error"
    })

    except Exception as e:
        print(f"Error during update: {e}")
        return jsonify({
            "error": str(e),
            "status": "critical_error"
        }), 500
    
@app.route('/api/stop_vibe')
def stop_vibe():
    try:
       from utils.spotify import stop_spotify
       success = stop_spotify(
            os.getenv("SPOTIPY_CLIENT_ID") or os.getenv("SPOTIFY_CLIENT_ID"),
            os.getenv("SPOTIPY_CLIENT_SECRET") or os.getenv("SPOTIFY_CLIENT_SECRET"),
            os.getenv("SPOTIPY_REDIRECT_URI") or os.getenv("SPOTIFY_REDIRECT_URI")
        )
       return jsonify({"status": "success" if success else "error"})
    except Exception as e:
        print(f"Stop error: {e}")
        return jsonify({"status": "error"}), 500  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)