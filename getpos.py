#!/usr/bin/env python3
# script coded by Phr34kz

import subprocess, time, os, sys, re, signal

try:
    import folium
    import selenium
    import webdriver_manager
except ImportError:
    os.system('pip3 install folium selenium webdriver-manager')

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Function to get GPS data using ADB
def get_gps_data():
    try:
        result = subprocess.run(["adb", "shell", "dumpsys", "location"], capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout
            gps_data = re.search(r'gps ([0-9.,-]+) hAcc', output)
            if gps_data:
                lat, lon = map(float, gps_data.group(1).split(','))
                return lat, lon
    except Exception as e:
        print(f"Error getting GPS data: {e}")
        return None, None

# Function to create and update the map
def update_map(lat, lon):
    if lat is None or lon is None:
        print("Invalid GPS data. Map not updated.")
        return
    m = folium.Map(location=[lat, lon], zoom_start=15)
    folium.Marker([lat, lon], popup="Your Location").add_to(m)
    m.save("gps_map.html")

# Function to check if Chromium is installed and install if not
def ensure_chromium():
    chromium_path = "/usr/bin/chromium"
    if not os.path.exists(chromium_path):
        print("Chromium not found. Attempting to install...")
        if sys.platform.startswith('linux'):
            try:
                subprocess.run(['sudo', 'apt-get', 'update'], check=True)
                subprocess.run(['sudo', 'apt-get', 'install', '-y', 'chromium'], check=True)
                print("Chromium installed successfully.")
            except subprocess.CalledProcessError:
                print("Failed to install Chromium. Please install it manually.")
                sys.exit(1)
        else:
            print("Automatic Chromium installation is only supported on Linux.")
            print("Please install Chromium manually and update the script with the correct path.")
            sys.exit(1)
    return chromium_path

# Function to handle Ctrl+C
def signal_handler(sig, frame):
    print("\nCtrl+C pressed. Cleaning up...")
    try:
        driver.quit()
    except:
        pass
    try:
        subprocess.run(["pkill", "chromium"], check=True)
    except:
        pass
    os.system('clear')
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

# Ensure Chromium is installed
chromium_path = ensure_chromium()

# Setup Selenium WebDriver
chrome_options = Options()
chrome_options.binary_location = chromium_path
chrome_options.add_experimental_option("detach", True)  # Keeps the browser open

driver = webdriver.Chrome(options=chrome_options)

# Initialize map with default location
default_lat, default_lon = 0, 0  # You can change this to a default location
update_map(default_lat, default_lon)
driver.get("file://" + os.path.abspath("gps_map.html"))

# Main loop to update GPS data and refresh the map
try:
    while True:
        lat, lon = get_gps_data()
        if lat is not None and lon is not None:
            update_map(lat, lon)
            driver.refresh()
        else:
            print("Waiting for valid GPS data...")
        time.sleep(3)  # Update every 3 seconds
except KeyboardInterrupt:
    signal_handler(signal.SIGINT, None)
