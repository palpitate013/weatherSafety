Weather Safety

Automatically shuts down your computer when a storm is detected using OpenWeatherMap, sends a mobile alert via ntfy, and reboots it via Wake-on-LAN from a remote device once the storm has passed.

Helps protect hardware during severe weather with minimal downtime.
Features

    🌩️ Detects storms using OpenWeatherMap

    🔕 Sends storm alerts to your phone via ntfy

    📴 Shuts down your main computer automatically

    🔁 Remotely reboots your main PC when the storm ends

    💡 Uses systemd for background execution and recovery

Requirements

    Linux (tested on Ubuntu)

    Python 3

    systemd

    wakeonlan utility (for remote script)

    An OpenWeatherMap API Key

    A valid ntfy topic name

    Wake-on-LAN enabled on your main PC

Installation
⚙️ Main PC Setup (Shutdown on Storm)

Run this on the PC you want to shut down during a storm:

bash <(curl -fsSL https://raw.githubusercontent.com/palpitate013/weatherSafety/main/install_main.sh)

This script:

    Downloads main.py

    Prompts for config (API key, location, ntfy topic, etc.)

    Sets up a Python virtual environment

    Installs required packages

    Creates a systemd service to run main.py

💻 Remote PC Setup (Wake After Storm)

Run this on a remote device that can send Wake-on-LAN packets:

bash <(curl -fsSL https://raw.githubusercontent.com/palpitate013/weatherSafety/main/install_remote.sh)

This script:

    Downloads remote.py

    Prompts for the same config as above

    Waits for the main PC to shut down

    Monitors weather and reboots the PC when it's safe

    Runs in the background via systemd

Configuration

After install, your config will be saved to:

/opt/weatherSafety/config.json

You can edit it manually if needed.

Sample:

{
  "weather": {
    "api_key": "your_api_key_here",
    "latitude": 35.2271,
    "longitude": -80.8431
  },
  "ntfy": {
    "topic": "storm-alert",
    "url": "https://ntfy.sh"
  },
  "computer": {
    "mac_address": "AA:BB:CC:DD:EE:FF",
    "hostname": "your-pc.local"
  }
}

🧹 Uninstallation
Main PC

To uninstall the Weather Safety script from your main PC, run:

bash <(curl -fsSL https://raw.githubusercontent.com/palpitate013/weatherSafety/main/uninstall_main.sh)

This will:

    Stop and disable the systemd service

    Remove the service file

    Delete the installation directory (/opt/weatherSafety)

    Reload the systemd daemon

Remote PC

To uninstall from the remote PC, run:

bash <(curl -fsSL https://raw.githubusercontent.com/palpitate013/weatherSafety/main/uninstall_remote.sh)

This performs the same steps as the main uninstall script but is intended for the remote Wake-on-LAN controller.
