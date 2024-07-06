## **PoGo GPS backend tool**

[![PoGo WiFi ADB GPS Track](https://img.youtube.com/vi/VIx5rJArMv0/0.jpg)](https://www.youtube.com/watch?v=VIx5rJArMv0 "PoGo WiFi ADB GPS Track")

< Click to watch PoC video >


Use with mock from Poly. Getting to know your current location wirelessly via a PC is now a breeze especially when you have the "Platinum Tier" and "Planet Earth" as a Geofence turned on.

───────────

### **Overview**


This Python script is designed to continuously track and display the GPS location of a device on a map on PC.
The script uses the Android Debug Bridge (ADB) to get the GPS data from the device, and then uses the Folium library to create an HTML map with the GPS location.
The map is displayed in a Chromium browser using Selenium WebDriver. 

Here is a breakdown of the functionality:

1. The script first checks if the required Python libraries (Folium, Selenium, and WebDriver Manager) are installed and installs them if they are not.

2. It defines a function `get_gps_data()` to get the GPS data from the device using ADB. The function runs the command `adb shell dumpsys location` and parses the output to get the latitude and longitude.

3. It defines a function `update_map(lat, lon)` to create an HTML map with the given latitude and longitude using Folium. The map is saved as `gps_map.html`.

4. It defines a function `ensure_chromium()` to check if Chromium is installed and installs it if it is not. The function supports automatic installation on Linux systems only.

5. It defines a function `signal_handler(sig, frame)` to handle the Ctrl+C signal. When Ctrl+C is pressed, the function quits the Selenium WebDriver and kills the Chromium process.

6. It registers the signal handler for the Ctrl+C signal.

7. It ensures that Chromium is installed.

8. It sets up the Selenium WebDriver to use Chromium.

9. It initializes the map with a default location (0, 0) and displays it in the Chromium browser.

10. It enters a main loop where it continuously gets the GPS data, updates the map, and refreshes the browser. The loop runs every 3 seconds.

11. If the script is interrupted with a KeyboardInterrupt (Ctrl+C), it calls the signal handler to clean up and exit.

───────────

### **Prerequisites**


• Python 3.x

• Linux-based operating system (or Windows WHL)                                                                                                   

• Sudo privileges for certain operations

• ADB, WiFi or via tethering

───────────

### **Usage**

Here are the steps to pair and connect to a device using ADB over WiFi:

1. On the Android device:
   - Enable Developer options if not already enabled
   - Go to Developer options and enable "Wireless debugging"
   - Tap on "Wireless debugging" to open the settings
   - Tap "Pair device with pairing code"
   - Note the IP address, port number, and pairing code shown

2. On your computer:
   - Open a command prompt/terminal 
   - Run the pairing command:
     ```
     adb pair <ip-address>:<port>
     ```
   - Enter the pairing code when prompted

3. After successful pairing:
   - On the Android device, note the IP address and port shown under "IP address & port"
   - On your computer, run:
     ```
     adb connect <ip-address>:<port>
     ```

4. You should now be connected wirelessly. Verify with:
   ```
   adb devices
   ```

Key things to note:
- The device and computer must be on the same WiFi network
- The pairing port is different from the connection port
- You may need to repeat the pairing process after device reboots
- Use "adb disconnect" when done to close the connection

This allows you to use ADB wirelessly without needing a USB cable connection.

──────────────────────

### **GUI version**

Getpos_gui.py is slow and a little unresponsive as compared to getpos.py

![image](https://github.com/kr4k0n/Pogo_GPS/assets/153607066/378a9504-d9ba-469f-88f4-ece9705b4278)


──────────────────────

### **Authors**


• Phr34kz  

───────────

### **Credits**

Angelina Tsuboi - Payload Interpreter cause I'm too lazy to type a readme https://payload-wizard.vercel.app/ ( https://github.com/ANG13T )
Curious? Watch her on Youtube https://youtu.be/U1-pOPFKcXo?si=nhZoMPZOQ3q-Y2Bc

──────────────────────────
