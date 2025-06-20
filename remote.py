import json
import requests

# Load config
with open('config.json') as f:
    config = json.load(f)

API_KEY = config['weather']['api_key']
LAT = config['weather']['latitude']
LON = config['weather']['longitude']
NTFY_TOPIC = config['ntfy']['topic']
NTFY_URL = f"{config['ntfy']['url']}/{NTFY_TOPIC}"

def check_storm(mock_weather=None):
    if mock_weather is None:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}"
        resp = requests.get(url)
        resp.raise_for_status()
        weather = resp.json()
    else:
        weather = mock_weather

    description = weather.get("weather", [{}])[0].get("description", "").lower()
    storm_keywords = ["thunderstorm", "tornado", "storm", "hail"]
    return any(keyword in description for keyword in storm_keywords)

def send_ntfy(message, title):
    headers = {
        "Title": title,
        "Priority": "urgent"
    }
    response = requests.post(NTFY_URL, headers=headers, data=message)
    response.raise_for_status()