import json
import uasyncio
import network
from time import sleep
from uAPI import uAPI, HTTPResponse
from picozero import pico_temp_sensor
wlan = network.WLAN(network.STA_IF)
while wlan.isconnected() == False:
    print('Waiting for connection...')
    sleep(1)
ip = wlan.ifconfig()[0]
print(f'Connected on {ip}')

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

try:
    uasyncio.run(api.run())
except KeyboardInterrupt:
    print("Stopping")
    api.stop()
except Exception as e:
    print("Error:", e)
    api.stop()