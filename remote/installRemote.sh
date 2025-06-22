#!/bin/bash
set -e

# Define variables
INSTALL_DIR="/opt/weatherSafety"
REPO_URL="https://raw.githubusercontent.com/palpitate013/weatherSafety/main/remote"
SERVICE_NAME="weatherSafety-remote"
VENV_DIR="$INSTALL_DIR/env"

echo "=== Weather Safety Remote Installer ==="

echo "Creating install directory at $INSTALL_DIR"
sudo mkdir -p "$INSTALL_DIR"
sudo chown "$(whoami):$(whoami)" "$INSTALL_DIR"

echo "Downloading remote.py..."
curl -fsSL "$REPO_URL/remote.py" -o "$INSTALL_DIR/remote.py"

# Ask for config values
read -p "Enter your OpenWeatherMap API Key: " API_KEY
read -p "Enter your latitude (e.g. 35.2271): " LAT
read -p "Enter your longitude (e.g. -80.8431): " LON
read -p "Enter your ntfy topic name (e.g. storm-alert): " TOPIC
read -p "Enter your computer hostname: " HOSTNAME
read -p "Enter your computer MAC address (e.g. AA:BB:CC:DD:EE:FF): " MAC

echo "Creating config.json..."
tee "$INSTALL_DIR/config.json" > /dev/null <<EOF
{
  "weather": {
    "api_key": "$API_KEY",
    "latitude": "$LAT",
    "longitude": "$LON"
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

echo "Creating virtual environment in $VENV_DIR"
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

echo "Installing Python dependencies..."
pip install requests wakeonlan

deactivate

echo "Creating systemd service..."
sudo tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null <<EOF
[Unit]
Description=Weather Safety Remote Script
After=network.target

[Service]
ExecStart=$VENV_DIR/bin/python $INSTALL_DIR/remote.py
WorkingDirectory=$INSTALL_DIR
Restart=always
RestartSec=10
User=$(whoami)

[Install]
WantedBy=multi-user.target
EOF

echo "Reloading systemd and enabling service..."
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl start "$SERVICE_NAME"

echo "✅ Weather Safety Remote setup complete!"
echo "Config file located at: $INSTALL_DIR/config.json"
echo "Check service status with: sudo systemctl status $SERVICE_NAME"
