# Raspberry Pi Pico W Temperature Server

This is a simple temperature server for the Raspberry Pi Pico W.  The temperature may be obtained at the `/temp` endpoint.

```
wget -q 192.168.1.83/temp -O /dev/stdout
{"unit": "C", "temp": 30.78955}
```

This works with https://github.com/edmcman/uAPI but I don't know how to actually
install this using the latest micropython version.

So I installed the main uAPI and then manually copied `application.py` which I
changed.