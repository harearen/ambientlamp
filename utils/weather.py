import requests

def fetch_london_weather(api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q=London,uk&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status() # エラーがあれば例外を投げる
        data = response.json()
        
        return {
            "status": data['weather'][0]['main'], # 例: "Rain", "Clouds", "Clear"
            "temp": data['main']['temp']           # 例: 12.5
        }
    except Exception as e:
        print(f"天気データの取得に失敗しました: {e}")
        return None