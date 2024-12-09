import uasyncio
import network
from time import sleep
from uAPI import uAPI, HTTPResponse
from picozero import pico_temp_sensor, pico_led
from secret import ssid, password

async def connect_to_wifi():    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    pico_led.blink()
    while not wlan.isconnected():
        print("Waiting for connection...")
        await uasyncio.sleep(1)
    print("Connected:", wlan.ifconfig())
    pico_led.on()
    return wlan

async def monitor_wifi():
    wlan = network.WLAN(network.STA_IF)

    while True:
        if not wlan.isconnected():
            print("Wi-Fi disconnected! Reconnecting...")
            await connect_to_wifi()
        await uasyncio.sleep(5)

api = uAPI(
    port=80,
    title="Hello uAPI!",
    description="My First API with uAPI.",
    version="1.0.0",
)

@api.endpoint("/test", "GET")
def hello_world():
    print("Console: Hello World!")
    return HTTPResponse(data="Hello world!", content_type="plain/text")

@api.endpoint("/temp", "GET")
def get_temp():
    print("Console: Getting Temp...")
    temp = pico_temp_sensor.temp
    response = {
        "temp": temp,
        "unit": "C",
    }
    return HTTPResponse(data=response)

async def main():
    await connect_to_wifi()
    monitor_task = uasyncio.create_task(monitor_wifi())
    await api.run()
try:
    uasyncio.run(main())
except KeyboardInterrupt:
    print("Stopping")
    api.stop()
except Exception as e:
    print("Error:", e)
    api.stop()