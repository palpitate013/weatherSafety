import json
import requests
import sys
import subprocess
import time

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

def shutdown():
    send_ntfy("Shutting down due to incoming storm.", "Storm Detected")
    subprocess.run(["sudo", "shutdown", "now"])

if __name__ == "__main__":
    try:
        print("Starting storm monitor loop (every 90 seconds)...")
        while True:
            try:
                if check_storm():
                    shutdown()
                else:
                    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] No storm detected.")
            except Exception as e:
                print(f"[ERROR] {e}", file=sys.stderr)
            time.sleep(90)
    except KeyboardInterrupt:
        print("Exiting on user interrupt.")
