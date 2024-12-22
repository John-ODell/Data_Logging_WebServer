import machine
import dht
import time

dht11 = dht.DHT11(machine.Pin(4))

while True:
    dht11.measure()
    temp_c = dht11.temperature()
    temp_f = (temp_c * 9/5) + 32
    humidity = dht11.humidity()
    print("Temperature (C):", temp_c)
    print("Temperature (F):", temp_f)
    print("Humidity (%):", humidity)
    time.sleep(1)
