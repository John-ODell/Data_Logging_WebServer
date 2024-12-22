import machine
import dht
import time
import sdcard
import uos
import bmp280

dht11 = dht.DHT11(machine.Pin(4))

i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21))
bmp = bmp280.BMP280(i2c)

sd = sdcard.SDCard(machine.SPI(2, sck=machine.Pin(14), mosi=machine.Pin(13), miso=machine.Pin(12)), machine.Pin(5))
uos.mount(sd, "/sd")

def log_data_csv(temp_f_dht, humidity, temp_f_bmp, pressure, avg_temp_f):
    with open("/sd/log.csv", "a") as log:
        log.write("{},{},{},{},{},{}\n".format(get_current_time(), temp_f_dht, humidity, temp_f_bmp, pressure, avg_temp_f))

def get_current_time():
    year, month, day, hour, minute, second, _, _ = time.localtime()
    return "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(year, month, day, hour, minute, second)


while True:
    dht11.measure()
    temp_c_dht = dht11.temperature()
    temp_f_dht = (temp_c_dht * 9/5) + 32
    humidity = dht11.humidity()

    temp_c_bmp = bmp.temperature
    temp_f_bmp = (temp_c_bmp * 9/5) + 32
    pressure = bmp.pressure
    
    avg_temp_f = (temp_f_dht + temp_f_bmp) / 2
    
    print("DHT11 - Temperature (F):", temp_f_dht, "Humidity (%):", humidity)
    print("BMP280 - Temperature (F):", temp_f_bmp, "Pressure (hPa):", pressure)
    print("Average Temperature (F):", avg_temp_f)
    
    log_data_csv(temp_f_dht, humidity, temp_f_bmp, pressure, avg_temp_f)
    
    time.sleep(60) # log readings every minute
