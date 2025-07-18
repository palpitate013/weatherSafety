import json
import requests
import subprocess
import time
import sys

# Load config
with open('config.json') as f:
    config = json.load(f)

API_KEY = config['weather']['api_key']
LAT = config['weather']['latitude']
LON = config['weather']['longitude']
NTFY_TOPIC = config['ntfy']['topic']
NTFY_URL = f"{config['ntfy']['url']}/{NTFY_TOPIC}"
PC_MAC = config['computer']['mac_address']
PC_NAME = config['computer']['hostname']

def is_main_pc_up():
    result = subprocess.run(
        ["ping", "-c", "1", "-W", "1", PC_NAME],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0

def wait_for_shutdown(ping_fail_threshold=3, interval=30):
    print(f"Monitoring {PC_NAME} for shutdown...")
    fail_count = 0
    while True:
        if is_main_pc_up():
            fail_count = 0
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {PC_NAME} is still online.")
        else:
            fail_count += 1
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Ping failed ({fail_count}/{ping_fail_threshold})")
            if fail_count >= ping_fail_threshold:
                print(f"{PC_NAME} appears to be offline. Starting storm monitor...")
                break
        time.sleep(interval)

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

def wake_pc(mac):
    subprocess.run(["wakeonlan", mac])

if __name__ == "__main__":
    try:
        wait_for_shutdown()

        print("Storm monitor started. Waiting for clear weather before rebooting main PC...")
        while True:
            try:
                if not check_storm():
                    wake_pc(PC_MAC)
                    send_ntfy(f"{PC_NAME} booting up as storm has passed.", "Storm Over")
                    break
                else:
                    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Storm still active, checking again in 10 minutes...")
            except Exception as e:
                print(f"[ERROR] Weather check failed: {e}", file=sys.stderr)

            time.sleep(600)  # 10 minutes
    except Exception as e:
        print(f"[FATAL ERROR] {e}", file=sys.stderr)
        sys.exit(1)
