## **PoGo GPS backend tool**

Use with mock location from Polygon

──────────────────────────

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


### **Authors**


• Phr34kz                                                                                                                                                                                    

──────────────────────────
