import os
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv

from utils.director import get_ai_vibe
from utils.weather import fetch_london_weather
# from utils.spotify import play_vibe
from utils.led_sim import hsv_to_rgb_normalized

load_dotenv()

app = Flask(__name__)
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/update_vibe')
def update_vibe():
    # 処理全体を try で囲む必要があります
    try:
        weather_info = fetch_london_weather(OPENWEATHER_API_KEY)
        if not weather_info:
            return jsonify({"error": "Failed to fetch weather data"}), 500

        vibe = get_ai_vibe(weather_info["status"], weather_info["temp"])

        # play_vibe(...)

        h = vibe.get("hue", 0)
        s = vibe.get("saturation", 0)
        v = vibe.get("brightness", 0)

        r, g, b = hsv_to_rgb_normalized(h, s, v)

        # フロントエンドに返すデータを整形
        return jsonify({
            "vibe_name": vibe["vibe_name"],
            "reason": vibe["reason"],
            "spotify_query": vibe["spotify_query"],
            "rgb": [r, g, b] 
        })

    except Exception as e:
        print(f"Error during update: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)