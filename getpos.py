#!/usr/bin/env python3
# script coded by Phr34kz

import subprocess, time, os, sys, re, signal

try:
    import folium
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    os.system('pip3 install folium selenium webdriver-manager')

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

def update_map(lat, lon, zoom):
    if lat is None or lon is None:
        print("Invalid GPS data. Map not updated.")
        return
    m = folium.Map(location=[lat, lon], zoom_start=zoom)
    folium.Marker([lat, lon], popup="Your Location").add_to(m)
    m.save("gps_map.html")

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

signal.signal(signal.SIGINT, signal_handler)

chromium_path = ensure_chromium()

chrome_options = Options()
chrome_options.binary_location = chromium_path
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

default_lat, default_lon = 0, 0
default_zoom = 15
current_zoom = default_zoom

update_map(default_lat, default_lon, current_zoom)
driver.get("file://" + os.path.abspath("gps_map.html"))

try:
    while True:
        lat, lon = get_gps_data()
        if lat is not None and lon is not None:
            # Wait for the map to be loaded
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "folium-map"))
            )
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "leaflet-control-zoom"))
            )
            
            # Update the map with the current zoom level
            update_map(lat, lon, current_zoom)
            driver.refresh()
            time.sleep(1)  # Add a short delay
            
            # Wait for the map to be reloaded
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "folium-map"))
            )
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "leaflet-control-zoom"))
            )
        else:
            print("Waiting for valid GPS data...")
        time.sleep(3)
except KeyboardInterrupt:
    signal_handler(signal.SIGINT, None)
