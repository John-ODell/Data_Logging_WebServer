ESP32 Data logging webserver by John O'Dell

Items Needed

    - ESP32
    - BMP280
    - DHT11
    - Micro SD Card Module
    - Breadboard
    - Jumper Wire (M to M and F to M)
    - Wi-fi Connection

The ESP32 generally does not fit into a standard breadboard. The best solution is to let one side hang over the rails and the other into the breadboard. 

Pin usage is not randomly chosen and can be different depending on models. Both the BMP280 and Micro SD Module use i2c communication. Please refer to your manufacturers guide and adjust accordingly.

Module used for this project: ESP32-WROOM-32D 38pin
Amazon: https://shorturl.at/EMIyV2 
Internationl: https://shorturl.at/Ojy6o

Download Thonny IDE : https://thonny.org/
    
    - Flash Micropython for your ESP device 
    - Skip to the "testing examples" section or follow the guide below

** Flashing Micropython

    - Open Thonny IDE
    - Plug in your device in bootloader mode
    - Navigate to the top left and click on "Run"
        - Configure Interpreter 
        - "Which Kind of interpreter?"
            - MicroPython (ESP32)
        - "Port of WebREPL"
            - Click the COMS Port, if there is none make sure your device is plugged in and in bootloader mode
        - Click "Install or Updtade MicroPython (esptool)"
        - Target port
            - Choose the device 
        - "MicroPython family"
            - ESP32 Generic or your specific version 
        - "variant"
            - Check your manufacturer
        - "version"
            - most recent version
    - Exit out of the conifgurater to the main page
    - Navigate back to the "Run" and "Configure Interpreter"
        - Choose the Coms port 
        - Press Ok
    - Return to the home page
    - Press the red stop sign
    - In the bottom serial your device will now be reconized and flashed with MicroPython
 

Testing Examples: Before testing you will need to save these requirments to your device

    - Open and Save the file "bmp280.py" to the device named as "bmp280.py"
    - Navigate to the "tools" at the top left
    - Click on "Manage Packages"
        - type "sdcard" and press enter
        - click on the package called "sdcard"
        - click install 

Open the "bmp280_example.py"

    PIN OUTS:
    VCC -> 3.3V
    GND -> GND
    SCL -> GPIO 22
    SDA -> GPIO 21

The Barometer and Temperature in C and F will be printed to the serial monitor. 

    - Troubleshooting
    - Softi2c is used in this example, depending on device may need to be adjust to i2c. 

Open the "dht11_example.py"

    PIN OUTS: 
    VCC -> 3.3v
    GND -> GND
    S -> GPIO 4

The Humidity and Temperature is printed to the serial monitor

    - there can be varying differences in the temperatures taken]
    - the BMP280 is more accurate with +-1
    - the DHT11 has a +-2
    - using the average in F is the best readout compared to an analog reading most of the time

Open the "data_logger.py" and place the Micro SD card into the breadboard

    PIN OUTS:
    VCC -> 3.3v
    GND -> GND
    SCK -> GPIO 14
    MOSI -> PGIO 13
    MISO -> GPIO 12

This example creates a csv file logging the bmp and dht11 readings on the SD card every minute. 

    - TROUBLESHOOTING
    - your device may not take i2csoft and need i2c
    - make sure your pins are in the correct places and the unit is powered at 3.3v
    - The example is used with a 2gb SD card, cards larger than 8gb may run into problems
    - The time stamp will be autoformated in excel, choose the first cell with ######## and press enter
    - remove the sd card to ensure the data was saved
    - delete the file before inserting the SD card into the module again

ESP32 Data Logging Web Server:

Open the sketch "http_data_download.py". Make sure you have the "bmp280.py" saved to the device named "bmp280.py" and the sdcard library from the library manager.

    - Follow the Pin Outs above
    - Replace the ssid and password with your wi-fi credientials
    - run the sketch (press the green arrow)
    - In the serial, a local host IP address will be given
        - Copy and paste into a browser
    - Displayed will be the real time data of the sensors and a dowload button the retrieve the CSV from the memory card
    - Refreshing the page will update the senors
    - data is logged once every minute along with a timestamp
        - to correct a ####### timestamp, open in excel, click on the first cell and hit enter
    - This sensors can be replaced by others, adjust the call and formatting for your data logging needs

    TROUBLESHOOTING
    - After stopping the script, you will need to wait ~1 minute for the port to open again.
    - if you have a file named "log.csv" before running the main script, it may not log correctly, make sure the SD card is empty before running.
    - Run all examples to ensure sensors and memory card are working
    - ESP32 modules are different, if needed flash generic MicroPython rather than the model specific if available


