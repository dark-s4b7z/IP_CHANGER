# -*- coding: utf-8 -*-

import time
import os
import subprocess
import sys

# requests + socks সাপোর্ট চেক + ইনস্টল
try:
    import requests
except ImportError:
    print('[+] Installing requests and requests[socks]...')
    os.system('pip3 install requests requests[socks] --break-system-packages')
    import requests
    print('[!] requests installed.')

# Tor চেক + ইনস্টল
try:
    subprocess.check_output(['which', 'tor'], stderr=subprocess.STDOUT)
except subprocess.CalledProcessError:
    print('[+] Installing tor...')
    os.system('apt update && apt install tor -y')
    print('[!] tor installed.')

os.system("clear")

def is_tor_running():
    try:
        subprocess.check_output(['systemctl', 'is-active', 'tor.service'])
        return True
    except:
        return False

def start_tor():
    if not is_tor_running():
        print("[+] Starting Tor service...")
        os.system("systemctl start tor")
        time.sleep(10)  # bootstrap-এর জন্য
        if is_tor_running():
            print("[+] Tor started.")
        else:
            print("[!] Tor failed to start. Run 'systemctl status tor' to check.")
            sys.exit(1)
    else:
        print("[+] Tor is already running.")

def get_ip():
    url = 'http://checkip.amazonaws.com'
    try:
        proxies = {'http': 'socks5h://127.0.0.1:9050', 'https': 'socks5h://127.0.0.1:9050'}
        r = requests.get(url, proxies=proxies, timeout=10)
        return r.text.strip()
    except Exception as e:
        return f"Error: {str(e)} (Check if Tor is running and SOCKS support installed)"

def change_ip():
    print("[+] Reloading Tor service for new IP...")
    os.system("systemctl reload tor")
    time.sleep(5)
    new_ip = get_ip()
    print(f"[+] Your IP has been Changed to : {new_ip}")

print('''\033[1;32;40m \n
  _________ ___ ___    _____  ________   ________  __      __ 
 /   _____//   |   \  /  _  \ \______ \  \_____  \/  \    /  \
 \_____  \/    ~    \/  /_\  \ |    |  \  /   |   \   \/\/   /
 /        \    Y    /    |    \|    `   \/    |    \        / 
/_______  /\___|_  /\____|__  /_______  /\_______  /\__/\  /  
        \/       \/         \/        \/         \/      \/   
                V 2.0 (DARK SHADOW)
from SHADOW
''')
print("\033[1;40;31m https://www.facebook.com/DARK.SHADOW.S4B7Z.143/\n")

# Tor স্টার্ট
start_tor()

print("\033[1;32;40m Use SOCKS5 proxy: 127.0.0.1:9050 \n")

while True:
    try:
        x = input("[+] Time to change IP in seconds [default=60] >> ").strip() or "60"
        lin = input("[+] How many times to change IP? (0 = infinite) >> ").strip() or "0"

        interval = int(x)
        times = int(lin)

        if times == 0:
            print("Starting infinite IP change. Press Ctrl+C to stop.")
            while True:
                change_ip()
                time.sleep(interval)
        else:
            for _ in range(times):
                change_ip()
                time.sleep(interval)

    except ValueError:
        print("Invalid number! Please enter valid integers.")
    except KeyboardInterrupt:
        print('\nAuto IP changer closed.')
        break
    except Exception as e:
        print(f"Error: {e}")
        break
