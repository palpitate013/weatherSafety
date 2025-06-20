#!/bin/bash
set -e

echo === Weather Safety Remote Installer ===

# Ask for config values
read -p "Enter your OpenWeatherMap API Key: " API_KEY
read -p "Enter your latitude (e.g. 35.2271): " LAT
read -p "Enter your longitude (e.g. -80.8431): " LON
read -p "Enter your ntfy topic name (e.g. storm-alert): " TOPIC
read -p "Enter your computer hostname: " HOSTNAME
read -p "Enter your computer MAC address (e.g. AA:BB:CC:DD:EE:FF): " MAC

# Write config file
cat > config.json <<EOF
{
  "weather": {
    "api_key": "$API_KEY",
    "latitude": $LAT,
    "longitude": $LON
  },
  "ntfy": {
    "topic": "$TOPIC",
    "url": "https://ntfy.sh"
  },
  "computer": {
    "mac_address": "$MAC",
    "hostname": "$HOSTNAME"
  }
}
EOF

# Set up virtual environment
echo "Creating virtual environment..."
python3 -m venv env
source env/bin/activate

# Install dependencies
pip install --upgrade pip
pip install requests

# Install wakeonlan
if ! command -v wakeonlan &> /dev/null; then
  echo "Installing wakeonlan..."
  sudo apt update
  sudo apt install -y wakeonlan
fi

echo "✅ Raspberry Pi setup complete!"
echo "Edit config.json if needed. Activate with: source env/bin/activate"
