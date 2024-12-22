import machine
import bmp280
import time

i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21))
bmp = bmp280.BMP280(i2c)

while True:
    temp_c = bmp.temperature
    temp_f = (temp_c * 9/5) + 32
    print("Temperature (C):", temp_c)
    print("Temperature (F):", temp_f)
    print("Pressure:", bmp.pressure)
    time.sleep(1)
