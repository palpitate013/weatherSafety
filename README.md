# 🌦️ Weather Safety

**Automatically shuts down your computer during storms to protect hardware and reboots it remotely when it's safe — with mobile alerts.**

---

## ✅ Key Features

* 🌩️ **Storm Detection** via OpenWeatherMap
* 📱 **Mobile Alerts** sent through [ntfy](https://ntfy.sh)
* 📴 **Auto Shutdown** of main PC when a storm is detected
* 🖥️ **Remote Wake-on-LAN** after storm passes
* 🔁 **Background Execution** with `systemd` for resilience

---

## 📋 Requirements

* 🐖 Linux (tested on Ubuntu)
* 🐍 Python 3
* 🖠️ `systemd`
* 🌐 OpenWeatherMap API Key
* 📣 A valid ntfy topic
* ⚡ `wakeonlan` utility (for remote machine)
* 🖥️ Wake-on-LAN enabled on your main PC

---

## ⚙️ Installation

### 🖥️ Main PC Setup — *Auto Shutdown on Storm*

Run this on the PC you want to protect:

```bash
bash <(curl -fsSL https://github.com/palpitate013/weatherSafety/raw/refs/heads/main/main/installMain.sh)
```

This script will:

* Download `main.py`
* Prompt for:

  * API key
  * Location (lat/lon)
  * ntfy topic
* Set up a Python virtual environment
* Install required packages
* Create a `systemd` service to run in the background

---

### 💻 Remote PC Setup — *Wake When Safe*

Run this on a separate device that can send Wake-on-LAN packets:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/palpitate013/weatherSafety/main/remote/installRemote.sh)
```

This script will:

* Download `remote.py`
* Prompt for the same config info
* Monitor weather conditions
* Reboot the main PC when safe
* Run continuously in the background via `systemd`

---

## ⚙️ Configuration

After install, your config will be saved to:

```plaintext
/opt/weatherSafety/config.json
```

### 📝 Sample Configuration:

```json
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
```

You can edit this file manually if needed.

---

## 🧹 Uninstallation

### 🖥️ Main PC

To remove Weather Safety from the main PC:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/palpitate013/weatherSafety/main/main/uninstallMain.sh)
```

This will:

* Stop and disable the `systemd` service
* Delete the service file
* Remove `/opt/weatherSafety`
* Reload `systemd` daemon

---

### 💻 Remote PC

To uninstall from the remote Wake-on-LAN device:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/palpitate013/weatherSafety/main/remote/uninstallRemote.sh)
```

Same steps as above, but targeted to the remote setup.

---
