<img width="734" height="241" alt="Untitled-6 (7)" src="https://github.com/user-attachments/assets/7d377551-2007-4083-b4d8-d1d6ac8b13a5" />

<div align="center">

# 📡 WIFITexp
### *WiFi Network Analyzer & Security Monitor*

<img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python Version">
<img src="https://img.shields.io/badge/Flask-3.0.0-green.svg" alt="Flask">
<img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg" alt="Platform">
<img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
<img src="https://img.shields.io/badge/Status-Active-success.svg" alt="Status">

*A powerful, real-time WiFi network monitoring tool that exposes detailed network information, connected devices, and security vulnerabilities with a beautiful web interface.*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots) • [Contributing](#-contributing)

---

</div>

## 🎯 Overview

**WIFITexp** is a sophisticated WiFi network analyzer built for penetration testers, network administrators, and security enthusiasts. It provides comprehensive real-time monitoring of your network infrastructure and surrounding WiFi environments with an intuitive, hacker-aesthetic web dashboard.

### Why WIFITexp?

- 🔍 **Complete Network Visibility** - See everything on your network in real-time
- 🛡️ **Security Assessment** - Automatically identify vulnerable networks
- 📊 **Channel Analytics** - Optimize your WiFi with heatmap visualization
- 🎨 **Beautiful UI** - Cyberpunk-themed dashboard with live updates
- 🚀 **Zero Configuration** - Auto-opens browser, works out of the box
- 💻 **Cross-Platform** - Windows, Linux, and macOS support

---

## ✨ Features

### 🏠 **Your Network - Full Exposure**
Get complete visibility into your own network:
- **Network Configuration**: BSSID, Local/Public IP, DNS, Gateway, Subnet
- **Connection Details**: Channel, Frequency, Bandwidth, Security Protocol
- **Device Tracking**: Real-time monitoring of all connected devices
- **MAC/IP Mapping**: Complete device identification with hostnames
- **Uptime Monitoring**: Track network stability and firmware info

### 📶 **Nearby Networks - Intelligence Gathering**
Scan and analyze surrounding WiFi networks:
- **Signal Strength Analysis**: dBm measurements with distance estimation
- **Security Assessment**: Identify WPA3/WPA2/WPA/Open networks
- **Vulnerability Detection**: Automatic risk level calculation
- **Channel Mapping**: See which channels are congested
- **Encryption Type**: AES, TKIP, or None detection

### 📊 **Advanced Analytics**
- **Channel Heatmap**: Visual representation of WiFi channel usage
- **Auto-Refresh**: Live data updates every 30 seconds
- **Risk Scoring**: Color-coded vulnerability indicators (🟢 Low, 🟡 Medium, 🔴 High)
- **Distance Calculation**: Estimate AP distance based on signal strength
- **Device Categorization**: Identify device types from MAC addresses

---

## 🚀 Installation

### Prerequisites

```bash
# Python 3.7 or higher required
python --version
```

### Quick Install

```bash
# Clone the repository
git clone https://github.com/Jack111I/WIFITexp.git
cd WIFITexp

# Install dependencies (only 2 packages!)
pip install -r requirements.txt

# Run the tool
python wifitexp_server.py
```

### Manual Installation

```bash
# Install packages individually
pip install Flask==3.0.0 Flask-CORS==4.0.0
```

### Platform-Specific Notes

**🪟 Windows**
- No additional setup required
- Uses built-in `netsh` and `arp` commands
- Run from Command Prompt or PowerShell

**🐧 Linux**
- Requires `sudo` for WiFi scanning
- Install NetworkManager: `sudo apt-get install network-manager`
- Run with elevated privileges: `sudo python3 wifitexp_server.py`

**🍎 macOS**
- Uses native `airport` utility
- Requires `sudo` for scanning
- May need to grant terminal location permissions

---

## 💻 Usage

### Basic Usage

```bash
# Start the server (browser opens automatically)
python wifitexp_server.py
```

**That's it!** The dashboard will automatically open at `http://localhost:5000`

### Advanced Usage

```bash
# Linux/Mac with elevated privileges
sudo python3 wifitexp_server.py

# Windows - Run as Administrator for better device detection
# Right-click > Run as Administrator
python wifitexp_server.py
```

### API Endpoints

WIFITexp provides a REST API for integration:

```bash
# Get cached data
GET http://localhost:5000/api/data

# Trigger new scan
GET http://localhost:5000/api/scan

# Get scanner status
GET http://localhost:5000/api/status
```

**Example Response:**
```json
{
  "my_network": {
    "ssid": "MyNetwork",
    "ip": "192.168.1.100",
    "gateway": "192.168.1.1",
    "security": "WPA2-Personal"
  },
  "connected_devices": [...],
  "nearby_networks": [...],
  "last_update": "2025-02-08T12:34:56"
}
```

---

## 📸 Screenshots

### Main Dashboard
<img width="734" height="241" alt="Untitled-6 (3)" src="https://github.com/user-attachments/assets/2d0dc4bb-0ce6-4dfc-b7c9-f1f66368db3b" />


### Network Analysis
<img width="734" height="241" alt="Untitled-6 (4)" src="https://github.com/user-attachments/assets/b7f7cc1f-5550-4968-81aa-9d2092e87b6f" />

<img width="734" height="241" alt="Untitled-6 (6)" src="https://github.com/user-attachments/assets/0b91c1b8-2f35-4df7-9d9e-8d68e775cd41" />


### Nearby Networks
<img width="734" height="241" alt="Untitled-6 (5)" src="https://github.com/user-attachments/assets/61ba26e8-bed5-43b0-9dbd-545bbd112f49" />


---

## 🛠️ Tech Stack

### Backend
- **Python 3.7+** - Core language
- **Flask 3.0.0** - Web framework
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **HTML5/CSS3** - Modern web standards
- **Vanilla JavaScript** - No frameworks, pure performance
- **Fetch API** - RESTful communication

### System Integration
- **subprocess** - System command execution
- **socket** - Network interface operations
- **webbrowser** - Auto-launch functionality
- **threading** - Concurrent operations

### Network Tools
- **Windows**: `netsh`, `ipconfig`, `arp`, `getmac`
- **Linux**: `nmcli`, `ip`, `arp`
- **macOS**: `airport`, `arp`

---

## 🔒 Security & Privacy

### What WIFITexp Does:
✅ Scans publicly broadcasted WiFi beacon frames  
✅ Uses ARP to detect devices on **YOUR** network only  
✅ Analyzes security configurations of nearby networks  
✅ Provides risk assessment based on encryption standards  

### What WIFITexp Does NOT Do:
❌ Crack passwords or break into networks  
❌ Capture network traffic or packets  
❌ Access devices on other networks  
❌ Perform any attacks or exploits  
❌ Store or transmit data externally  

**Legal Notice**: This tool is for **educational purposes** and **authorized network monitoring only**. Users are responsible for complying with local laws and regulations. Only scan networks you own or have explicit permission to monitor.

---

## 📊 Dashboard Features Breakdown

### Status Bar
- **Scanning Status**: Live indicator with pulse animation
- **Device Count**: Total connected devices
- **Network Count**: Nearby networks detected
- **Last Update**: Timestamp of most recent scan

### Your Network Panel
- **Network Header**: SSID with security badge
- **Info Grid**: 12+ network parameters
- **Device Table**: Sortable list of connected devices
- **Real-time Updates**: Auto-refresh every 30 seconds

### Nearby Networks Section
- **Network Cards**: Individual cards for each detected network
- **Signal Bars**: Visual signal strength indicator
- **Risk Badges**: Color-coded vulnerability assessment
- **Detailed Info**: MAC, channel, security, encryption, distance

### Channel Heatmap
- **Interactive Graph**: Hover for network count
- **11 Channels**: 2.4GHz band visualization
- **Congestion Detection**: Identify optimal channels
- **Real-time Updates**: Reflects current environment

---

## BUHAHHAHAHAHHAHHHAHAAAA 

## 🔧 Configuration

### Auto-Refresh Interval
Modify in `wifitexp_dashboard.html`:
```javascript
// Change refresh interval (default: 30000ms = 30 seconds)
setInterval(async () => {
    const data = await fetchData();
    if (data) updateDashboard(data);
}, 30000); // ← Change this value
```

### Server Port
Modify in `wifitexp_server.py`:
```python
# Change default port (default: 5000)
app.run(host='0.0.0.0', port=5000)  # ← Change port number
```

### Browser Auto-Open Delay
Modify in `wifitexp_server.py`:
```python
def open_browser():
    time.sleep(2)  # ← Adjust delay in seconds
    webbrowser.open('http://localhost:5000')
```

---

## 🐛 Troubleshooting

### "No networks found"
**Windows:**
- Ensure WiFi is enabled
- Run Command Prompt as Administrator

**Linux:**
```bash
sudo apt-get install network-manager
sudo systemctl start NetworkManager
```

**macOS:**
- Grant Terminal location permissions
- System Preferences → Security & Privacy → Location Services

### "Permission denied"
**Linux/macOS:**
```bash
# Always use sudo for WiFi scanning
sudo python3 wifitexp_server.py
```

### "Port already in use"
```bash
# Kill process on port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### "Module not found"
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Browser doesn't open automatically
- Manually navigate to `http://localhost:5000`
- Check firewall settings
- Try different browser as default

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Bugs
- Use the [GitHub Issues](https://github.com/Jack111i/WIFITexp/issues) page
- Include OS version, Python version, and error messages
- Provide steps to reproduce

### Feature Requests
- Open an issue with the `enhancement` label
- Describe the feature and use case
- Explain why it would be valuable

### Pull Requests
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/Jack111I/WIFITexp.git
cd WIFITexp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install in development mode
pip install -r requirements.txt
```

---

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 WIFITexp

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🙏 Acknowledgments

- **Flask Team** - For the excellent web framework
- **Python Community** - For comprehensive networking libraries
- **Open Source Contributors** - For inspiration and code patterns
- **Security Researchers** - For WiFi security best practices

---

## 📞 Support

### Get Help
- 💬 Instagram: @x_sayo-26 call me there xp

### Stay Updated
- ⭐ Star this repository
- 👀 Watch for updates
- 🔔 Enable notifications

---


---

<div align="center">

### 🌟 If you found this useful, please star the repo! 🌟

**Made with ❤️ by the SAYO**

*Hack the Planet* 🌐🔓

</div>

---


---

<div align="center">

**Remember**: There's nothing can't be exposed in that world and there's no privacy at all. So, be safe be updated.

© 2025 WIFITexp. All rights reserved.

</div>
