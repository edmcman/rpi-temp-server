# Raspberry Pi Pico W Temperature Server

This is a simple temperature server for the Raspberry Pi Pico W.  The temperature may be obtained at the `/temp` endpoint.

```
wget -q 192.168.1.83/temp -O /dev/stdout
{"unit": "C", "temp": 30.78955}
```

At the time of writing (December 2024), the official uAPI repository had some bugs and did not work for me.  This project expects to be used with my fork of the uAPI repository, [edmcman/uAPI](https://github.com/edmcman/uAPI).

## Install

I recommend using:
`pipkin --port /dev/ttyACM0 install -r requirements.txt`.

Then copy `main.py` and `secret.py` to the Raspberry Pi Pico W.
