#!/usr/bin/env python3
"""
WIFITexp Backend Server
Scans WiFi networks and monitors connected devices
"""

from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS
import subprocess
import re
import socket
import platform
import threading
import time
from datetime import datetime, timedelta
import json
import webbrowser

app = Flask(__name__)
CORS(app)

class WiFiScanner:
    def __init__(self):
        self.os_type = platform.system()
        self.cached_data = {
            'my_network': {},
            'connected_devices': [],
            'nearby_networks': [],
            'last_update': None
        }
        self.scanning = False
        
    def get_default_gateway(self):
        """Get the default gateway (router) IP address"""
        try:
            if self.os_type == "Windows":
                result = subprocess.run(['ipconfig'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'Default Gateway' in line or 'Passerelle par défaut' in line:
                        parts = line.split(':')
                        if len(parts) > 1:
                            gateway = parts[1].strip()
                            if gateway and gateway != '':
                                return gateway
            else:
                # Linux/Mac
                result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'default' in line:
                        parts = line.split()
                        if len(parts) > 2:
                            return parts[2]
        except:
            pass
        return "192.168.1.1"
    
    def get_local_ip(self):
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return "127.0.0.1"
    
    def get_public_ip(self):
        """Get public IP address"""
        try:
            import urllib.request
            return urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
        except:
            return "N/A"
    
    def get_network_interface(self):
        """Get the active network interface"""
        try:
            if self.os_type == "Windows":
                result = subprocess.run(['ipconfig'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'Wireless LAN adapter' in line or 'Ethernet adapter' in line:
                        return line.split(':')[0].strip()
            else:
                result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'default' in line:
                        parts = line.split()
                        if 'dev' in parts:
                            idx = parts.index('dev')
                            if idx + 1 < len(parts):
                                return parts[idx + 1]
        except:
            pass
        return None
    
    def scan_wifi_linux(self):
        """Scan WiFi networks on Linux using iwlist or nmcli"""
        networks = []
        try:
            # Try using nmcli first (more reliable)
            result = subprocess.run(['nmcli', '-f', 'SSID,BSSID,CHAN,SIGNAL,SECURITY', 'dev', 'wifi', 'list'],
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 4:
                        ssid = parts[0] if parts[0] != '--' else 'Hidden Network'
                        bssid = parts[1] if len(parts) > 1 else 'Unknown'
                        channel = parts[2] if len(parts) > 2 else '0'
                        signal = parts[3] if len(parts) > 3 else '-100'
                        security = ' '.join(parts[4:]) if len(parts) > 4 else 'Open'
                        
                        # Calculate risk based on security
                        risk = 'low'
                        if 'WPA3' in security:
                            risk = 'low'
                        elif 'WPA2' in security:
                            risk = 'low'
                        elif 'WPA' in security or 'WEP' in security:
                            risk = 'medium'
                        elif security == 'Open' or security == '--':
                            risk = 'high'
                        
                        # Estimate distance based on signal strength
                        try:
                            sig_val = int(signal)
                            if sig_val > -50:
                                distance = "~5-10m"
                            elif sig_val > -60:
                                distance = "~10-20m"
                            elif sig_val > -70:
                                distance = "~20-35m"
                            elif sig_val > -80:
                                distance = "~35-50m"
                            else:
                                distance = "~50m+"
                        except:
                            distance = "Unknown"
                        
                        networks.append({
                            'ssid': ssid,
                            'mac': bssid,
                            'channel': channel,
                            'signal': signal,
                            'security': security if security else 'Open',
                            'encryption': 'AES' if 'WPA2' in security or 'WPA3' in security else 'TKIP' if 'WPA' in security else 'None',
                            'risk': risk,
                            'distance': distance
                        })
        except Exception as e:
            print(f"Error scanning WiFi (Linux): {e}")
        
        return networks
    
    def scan_wifi_windows(self):
        """Scan WiFi networks on Windows using netsh"""
        networks = []
        try:
            result = subprocess.run(['netsh', 'wlan', 'show', 'networks', 'mode=bssid'],
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                current_ssid = None
                current_network = {}
                
                for line in result.stdout.split('\n'):
                    line = line.strip()
                    
                    if line.startswith('SSID'):
                        if current_network and current_ssid:
                            networks.append(current_network)
                        parts = line.split(':', 1)
                        current_ssid = parts[1].strip() if len(parts) > 1 else 'Hidden'
                        current_network = {'ssid': current_ssid}
                    
                    elif 'BSSID' in line and ':' in line:
                        parts = line.split(':', 1)
                        if len(parts) > 1:
                            bssid = parts[1].strip()
                            current_network['mac'] = bssid
                    
                    elif 'Signal' in line:
                        parts = line.split(':', 1)
                        if len(parts) > 1:
                            signal_percent = parts[1].strip().replace('%', '')
                            try:
                                # Convert percentage to dBm (approximation)
                                signal_dbm = int((int(signal_percent) / 2) - 100)
                                current_network['signal'] = str(signal_dbm)
                            except:
                                current_network['signal'] = '-70'
                    
                    elif 'Authentication' in line:
                        parts = line.split(':', 1)
                        if len(parts) > 1:
                            auth = parts[1].strip()
                            current_network['security'] = auth
                            
                            # Determine risk
                            risk = 'low'
                            if 'WPA3' in auth:
                                risk = 'low'
                            elif 'WPA2' in auth:
                                risk = 'low'
                            elif 'WPA' in auth:
                                risk = 'medium'
                            elif 'Open' in auth:
                                risk = 'high'
                            current_network['risk'] = risk
                    
                    elif 'Channel' in line:
                        parts = line.split(':', 1)
                        if len(parts) > 1:
                            current_network['channel'] = parts[1].strip()
                
                if current_network and current_ssid:
                    networks.append(current_network)
                
                # Fill in missing fields
                for net in networks:
                    if 'signal' not in net:
                        net['signal'] = '-70'
                    if 'channel' not in net:
                        net['channel'] = '0'
                    if 'security' not in net:
                        net['security'] = 'Unknown'
                    if 'risk' not in net:
                        net['risk'] = 'medium'
                    if 'mac' not in net:
                        net['mac'] = 'Unknown'
                    
                    # Add encryption and distance
                    net['encryption'] = 'AES' if 'WPA2' in net['security'] or 'WPA3' in net['security'] else 'TKIP' if 'WPA' in net['security'] else 'None'
                    
                    try:
                        sig_val = int(net['signal'])
                        if sig_val > -50:
                            net['distance'] = "~5-10m"
                        elif sig_val > -60:
                            net['distance'] = "~10-20m"
                        elif sig_val > -70:
                            net['distance'] = "~20-35m"
                        elif sig_val > -80:
                            net['distance'] = "~35-50m"
                        else:
                            net['distance'] = "~50m+"
                    except:
                        net['distance'] = "Unknown"
        
        except Exception as e:
            print(f"Error scanning WiFi (Windows): {e}")
        
        return networks
    
    def scan_wifi_macos(self):
        """Scan WiFi networks on macOS"""
        networks = []
        try:
            result = subprocess.run(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-s'],
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 5:
                        ssid = parts[0]
                        bssid = parts[1]
                        signal = parts[2]
                        channel = parts[3]
                        security = ' '.join(parts[6:]) if len(parts) > 6 else 'Open'
                        
                        risk = 'low'
                        if 'WPA3' in security:
                            risk = 'low'
                        elif 'WPA2' in security:
                            risk = 'low'
                        elif 'WPA' in security:
                            risk = 'medium'
                        else:
                            risk = 'high'
                        
                        try:
                            sig_val = int(signal)
                            if sig_val > -50:
                                distance = "~5-10m"
                            elif sig_val > -60:
                                distance = "~10-20m"
                            elif sig_val > -70:
                                distance = "~20-35m"
                            elif sig_val > -80:
                                distance = "~35-50m"
                            else:
                                distance = "~50m+"
                        except:
                            distance = "Unknown"
                        
                        networks.append({
                            'ssid': ssid,
                            'mac': bssid,
                            'channel': channel,
                            'signal': signal,
                            'security': security,
                            'encryption': 'AES' if 'WPA2' in security or 'WPA3' in security else 'TKIP' if 'WPA' in security else 'None',
                            'risk': risk,
                            'distance': distance
                        })
        except Exception as e:
            print(f"Error scanning WiFi (macOS): {e}")
        
        return networks
    
    def scan_nearby_networks(self):
        """Scan nearby WiFi networks based on OS"""
        if self.os_type == "Linux":
            return self.scan_wifi_linux()
        elif self.os_type == "Windows":
            return self.scan_wifi_windows()
        elif self.os_type == "Darwin":  # macOS
            return self.scan_wifi_macos()
        else:
            return []
    
    def get_connected_ssid(self):
        """Get currently connected WiFi SSID"""
        try:
            if self.os_type == "Linux":
                result = subprocess.run(['nmcli', '-t', '-f', 'active,ssid', 'dev', 'wifi'],
                                      capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if line.startswith('yes:'):
                        return line.split(':', 1)[1]
            
            elif self.os_type == "Windows":
                result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'],
                                      capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'SSID' in line and 'BSSID' not in line:
                        return line.split(':', 1)[1].strip()
            
            elif self.os_type == "Darwin":
                result = subprocess.run(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'],
                                      capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if ' SSID:' in line:
                        return line.split(':', 1)[1].strip()
        except:
            pass
        
        return "Unknown Network"
    
    def scan_local_devices(self):
        """Scan devices on local network using ARP"""
        devices = []
        try:
            # Get local network info
            local_ip = self.get_local_ip()
            network_prefix = '.'.join(local_ip.split('.')[0:3])
            
            # Use ARP to find devices
            if self.os_type == "Windows":
                result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
            else:
                result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
            
            device_count = 0
            for line in result.stdout.split('\n'):
                # Parse ARP output
                if self.os_type == "Windows":
                    match = re.search(r'(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F-]+)', line)
                else:
                    match = re.search(r'\((\d+\.\d+\.\d+\.\d+)\).*?([0-9a-fA-F:]+)', line)
                
                if match:
                    ip = match.group(1)
                    mac = match.group(2)
                    
                    # Filter only local network IPs
                    if ip.startswith(network_prefix):
                        device_count += 1
                        
                        # Try to get hostname
                        try:
                            hostname = socket.gethostbyaddr(ip)[0]
                        except:
                            hostname = f"Device-{device_count}"
                        
                        # Determine device type based on MAC vendor (simplified)
                        device_type = "Unknown"
                        connection_type = "WiFi"
                        signal = "Good"
                        
                        # Common MAC prefixes (simplified)
                        mac_upper = mac.upper()
                        if any(x in mac_upper for x in ['Apple', '00:1C:B3', '00:1E:C2']):
                            device_type = "Apple Device"
                        elif any(x in mac_upper for x in ['Samsung', '00:12:FB']):
                            device_type = "Samsung Device"
                        
                        devices.append({
                            'name': hostname,
                            'ip': ip,
                            'mac': mac,
                            'type': connection_type,
                            'signal': signal,
                            'status': 'Active'
                        })
        
        except Exception as e:
            print(f"Error scanning devices: {e}")
        
        # If no devices found, add at least the current device
        if len(devices) == 0:
            local_ip = self.get_local_ip()
            devices.append({
                'name': socket.gethostname(),
                'ip': local_ip,
                'mac': self.get_mac_address(),
                'type': 'WiFi',
                'signal': 'Excellent',
                'status': 'Active (This Device)'
            })
        
        return devices
    
    def get_mac_address(self):
        """Get MAC address of default interface"""
        try:
            if self.os_type == "Windows":
                result = subprocess.run(['getmac'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'Wi-Fi' in line or 'Ethernet' in line:
                        parts = line.split()
                        if len(parts) > 0:
                            mac = parts[0]
                            if '-' in mac:
                                return mac
            else:
                result = subprocess.run(['ip', 'link', 'show'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'link/ether' in line:
                        parts = line.split()
                        if len(parts) > 1:
                            return parts[1]
        except:
            pass
        return "Unknown"
    
    def get_my_network_info(self):
        """Get detailed info about current network"""
        try:
            local_ip = self.get_local_ip()
            gateway = self.get_default_gateway()
            ssid = self.get_connected_ssid()
            mac = self.get_mac_address()
            public_ip = self.get_public_ip()
            
            # Get DNS servers
            dns_servers = "8.8.8.8, 1.1.1.1"  # Default
            try:
                if self.os_type == "Linux":
                    with open('/etc/resolv.conf', 'r') as f:
                        dns_list = []
                        for line in f:
                            if line.startswith('nameserver'):
                                dns_list.append(line.split()[1])
                        if dns_list:
                            dns_servers = ', '.join(dns_list[:2])
                elif self.os_type == "Windows":
                    result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True)
                    dns_list = []
                    for line in result.stdout.split('\n'):
                        if 'DNS Servers' in line:
                            dns = line.split(':', 1)[1].strip()
                            dns_list.append(dns)
                    if dns_list:
                        dns_servers = ', '.join(dns_list[:2])
            except:
                pass
            
            return {
                'ssid': ssid,
                'bssid': mac,
                'ip': local_ip,
                'publicIP': public_ip,
                'dns': dns_servers,
                'gateway': gateway,
                'subnet': '255.255.255.0',
                'channel': '6',
                'frequency': '2.4 GHz',
                'bandwidth': '40 MHz',
                'security': 'WPA2-Personal',
                'encryption': 'AES-CCMP',
                'uptime': self.get_uptime(),
                'firmware': 'Auto-detected',
                'throughput': 'N/A'
            }
        except Exception as e:
            print(f"Error getting network info: {e}")
            return {}
    
    def get_uptime(self):
        """Get system uptime"""
        try:
            if self.os_type == "Linux":
                with open('/proc/uptime', 'r') as f:
                    uptime_seconds = float(f.readline().split()[0])
                    uptime = str(timedelta(seconds=int(uptime_seconds)))
                    return uptime
            elif self.os_type == "Windows":
                result = subprocess.run(['net', 'statistics', 'workstation'], 
                                      capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'Statistics since' in line:
                        return "See System Info"
        except:
            pass
        return "Unknown"
    
    def scan_all(self):
        """Perform complete scan"""
        print("Starting WiFi scan...")
        self.scanning = True
        
        try:
            self.cached_data['my_network'] = self.get_my_network_info()
            self.cached_data['connected_devices'] = self.scan_local_devices()
            self.cached_data['nearby_networks'] = self.scan_nearby_networks()
            self.cached_data['last_update'] = datetime.now().isoformat()
            print(f"Scan complete: Found {len(self.cached_data['connected_devices'])} devices, {len(self.cached_data['nearby_networks'])} networks")
        except Exception as e:
            print(f"Error during scan: {e}")
        
        self.scanning = False
        return self.cached_data

# Initialize scanner
scanner = WiFiScanner()

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'wifitexp_dashboard.html')

@app.route('/api/scan')
def scan():
    """Trigger a new scan and return results"""
    data = scanner.scan_all()
    return jsonify(data)

@app.route('/api/data')
def get_data():
    """Get cached data"""
    if not scanner.cached_data['last_update']:
        # First time, do a scan
        return jsonify(scanner.scan_all())
    return jsonify(scanner.cached_data)

@app.route('/api/status')
def status():
    """Get scanner status"""
    return jsonify({
        'scanning': scanner.scanning,
        'last_update': scanner.cached_data.get('last_update'),
        'os_type': scanner.os_type
    })

def open_browser():
    """Open browser automatically after a short delay"""
    time.sleep(1.5)  # Wait for server to start
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("=" * 60)
    print("WIFITexp Server Starting...")
    print("=" * 60)
    print(f"Operating System: {scanner.os_type}")
    print(f"Local IP: {scanner.get_local_ip()}")
    print(f"Gateway: {scanner.get_default_gateway()}")
    print()
    print("Performing initial scan...")
    scanner.scan_all()
    print()
    print("Server ready!")
    print("Opening dashboard in your browser...")
    print("Dashboard URL: http://localhost:5000")
    print("=" * 60)
    
    # Open browser automatically
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Start Flask server
    app.run(host='0.0.0.0', port=5000, debug=False)