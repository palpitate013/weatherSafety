#!/bin/bash
set -e

SERVICE_NAME="weatherSafety"
INSTALL_DIR="/opt/weatherSafety"

echo "=== Weather Safety Main Uninstall ==="

# Stop and disable the systemd service
echo "Stopping and disabling systemd service..."
sudo systemctl stop "$SERVICE_NAME" || true
sudo systemctl disable "$SERVICE_NAME" || true
sudo rm -f "/etc/systemd/system/${SERVICE_NAME}.service"

# Reload systemd
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload
sudo systemctl reset-failed

# Remove files and directories
echo "Removing install directory..."
sudo rm -rf "$INSTALL_DIR"

echo "✅ weatherSafety has been uninstalled."
