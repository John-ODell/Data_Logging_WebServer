import machine
import dht
import time
import sdcard
import uos
import bmp280
import network
import usocket as socket

dht11 = dht.DHT11(machine.Pin(4))

i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21))
bmp = bmp280.BMP280(i2c)

sd = sdcard.SDCard(machine.SPI(2, sck=machine.Pin(14), mosi=machine.Pin(13), miso=machine.Pin(12)), machine.Pin(5))
uos.mount(sd, "/sd")

# Connect to Wi-Fi
ssid = "**********"
password = "**********"
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    time.sleep(1)

print('Network config:', wlan.ifconfig())

def log_data_csv(temp_f_dht, humidity, temp_f_bmp, pressure, avg_temp_f):
    with open("/sd/log.csv", "a") as log:
        log.write("{},{},{},{},{},{}\n".format(get_current_time(), temp_f_dht, humidity, temp_f_bmp, pressure, avg_temp_f))

def get_current_time():
    year, month, day, hour, minute, second, _, _ = time.localtime()
    return "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(year, month, day, hour, minute, second)

def get_sensor_readings():
    dht11.measure()
    temp_c_dht = dht11.temperature()
    temp_f_dht = (temp_c_dht * 9/5) + 32
    humidity = dht11.humidity()
    temp_c_bmp = bmp.temperature
    temp_f_bmp = (temp_c_bmp * 9/5) + 32
    pressure = bmp.pressure
    avg_temp_f = (temp_f_dht + temp_f_bmp) / 2
    return temp_f_dht, humidity, temp_f_bmp, pressure, avg_temp_f

def web_page(temp_f_dht, humidity, temp_f_bmp, pressure, avg_temp_f):
    html = """<html><head><title>ESP32 Sensor Readings</title></head><body>
    <h1>ESP32 Sensor Readings</h1>
    <p>DHT11 - Temperature (F): {:.2f}</p>
    <p>DHT11 - Humidity (%): {:.2f}</p>
    <p>BMP280 - Temperature (F): {:.2f}</p>
    <p>BMP280 - Pressure (hPa): {:.2f}</p>
    <p>Average Temperature (F): {:.2f}</p>
    <a href="/download">Download Log</a>
    </body></html>""".format(temp_f_dht, humidity, temp_f_bmp, pressure, avg_temp_f)
    return html

def serve():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    
    while True:
        cl, addr = s.accept()
        request = cl.recv(1024)
        request = str(request)
        
        if "/download" in request:
            with open("/sd/log.csv", "r") as file:
                cl.send("HTTP/1.1 200 OK\r\n")
                cl.send("Content-Type: application/octet-stream\r\n")
                cl.send("Content-Disposition: attachment; filename=log.csv\r\n")
                cl.send("\r\n")
                cl.send(file.read())
        else:
            temp_f_dht, humidity, temp_f_bmp, pressure, avg_temp_f = get_sensor_readings()
            response = web_page(temp_f_dht, humidity, temp_f_bmp, pressure, avg_temp_f)
            cl.send("HTTP/1.1 200 OK\r\n")
            cl.send("Content-Type: text/html\r\n")
            cl.send("Connection: close\r\n")
            cl.send("\r\n")
            cl.sendall(response)
        
        cl.close()

import _thread
_thread.start_new_thread(serve, ())

while True:
    temp_f_dht, humidity, temp_f_bmp, pressure, avg_temp_f = get_sensor_readings()
    log_data_csv(temp_f_dht, humidity, temp_f_bmp, pressure, avg_temp_f)
    time.sleep(60)  # log readings every minute, refresh http page for real time reading update
