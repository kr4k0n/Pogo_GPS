#!/usr/bin/env python3
# script coded by Phr34kz

import subprocess, time, os, sys, re, signal, io
import threading
import folium
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def install_dependencies():
    required_packages = ['folium', 'pillow']
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"{package} not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_dependencies()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

clear_terminal()

def check_adb():
    try:
        subprocess.run(["adb", "version"], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        print("Error: ADB is not installed or not in the system path.")
        sys.exit(1)

check_adb()

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

class MapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Phr34kz PoGo Poly GPS Tracker")
        
        self.zoom_level = 15
        self.lat, self.lon = 0, 0
        self.map_cache = {}
        
        self.map_label = ttk.Label(self.root)
        self.map_label.pack(pady=10)
        
        self.coordinates_label = ttk.Label(self.root, text="Initializing...")
        self.coordinates_label.pack(pady=5)
        
        zoom_frame = ttk.Frame(self.root)
        zoom_frame.pack(pady=5)
        
        ttk.Button(zoom_frame, text="+", command=self.zoom_in).pack(side=tk.LEFT, padx=5)
        ttk.Button(zoom_frame, text="-", command=self.zoom_out).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(self.root, text="Quit", command=self.quit_app).pack(pady=5)
        
        self.gps_thread = threading.Thread(target=self.update_gps, daemon=True)
        self.gps_thread.start()

    def update_map(self):
        cache_key = (self.lat, self.lon, self.zoom_level)
        if cache_key in self.map_cache:
            photo = self.map_cache[cache_key]
        else:
            m = folium.Map(location=[self.lat, self.lon], zoom_start=self.zoom_level)
            folium.Marker([self.lat, self.lon], popup="Your Location").add_to(m)
            
            img_data = m._to_png(5)
            img = Image.open(io.BytesIO(img_data))
            img = img.resize((800, 500), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.map_cache[cache_key] = photo

        self.map_label.config(image=photo)
        self.map_label.image = photo
        
        self.coordinates_label.config(text=f"Latitude: {self.lat:.6f}, Longitude: {self.lon:.6f}, Zoom: {self.zoom_level}")

    def update_gps(self):
        while True:
            lat, lon = get_gps_data()
            if lat is not None and lon is not None:
                self.lat, self.lon = lat, lon
                self.root.after(0, self.update_map)
            else:
                self.root.after(0, lambda: self.coordinates_label.config(text="Waiting for valid GPS data..."))
            time.sleep(10)  # Update every 10 seconds

    def zoom_in(self):
        self.zoom_level = min(self.zoom_level + 1, 18)
        self.update_map()

    def zoom_out(self):
        self.zoom_level = max(self.zoom_level - 1, 3)
        self.update_map()

    def quit_app(self):
        self.root.quit()
        clear_terminal()
        sys.exit(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = MapApp(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Cleaning up...")
    finally:
        clear_terminal()
        sys.exit(0)
