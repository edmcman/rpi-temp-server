import uasyncio
import network
from uAPI import uAPI, HTTPResponse
import os
from picozero import pico_temp_sensor, pico_led
import random

ssid = 'verycreative-lr'
password = '03141005'

pms = random.choice(["None", "0xa11140", "network.WLAN.PM_NONE", "network.WLAN.PM_PERFORMANCE", "network.WLAN.PM_POWERSAVE"])
print(f"Random selected PM: {pms}")
pm = eval(pms)

async def connect_to_wifi():
    pico_led.off()
    wlan = network.WLAN(network.STA_IF)
    wlan.config(trace=1)
    wlan.active(True)
    if pm is not None: wlan.config(pm=pm)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pico_led.blink()
        print("Waiting for connection...")
        await uasyncio.sleep(1)
    print("Connected:", wlan.ifconfig())
    print(f"Actual PM: {hex(wlan.config('pm'))}")
    pico_led.on()
    return wlan

async def monitor_wifi():
    wlan = network.WLAN(network.STA_IF)

    c = 0
    while True:
        c += 1
        if c % 20 == 0:
            print("Still checking Wi-Fi connection...")
            print(f"Debug: connected: {wlan.isconnected()} status: {wlan.status()}")
            print(f"Actual PM: {hex(wlan.config('pm'))}")
        pico_led.off()
        await uasyncio.sleep(2)
        if not wlan.isconnected():
            print("Wi-Fi disconnected! Reconnecting...")
            await connect_to_wifi()
        else:
            pico_led.on()
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
    print(f"Starting server. OS: {os.uname()} PM: {pm}")
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