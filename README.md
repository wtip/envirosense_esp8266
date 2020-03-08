# EnviroSense ESP8266 - Environmental sensing WiFi IoT board
This current iteration is using a [NodeMCU](https://en.wikipedia.org/wiki/NodeMCU) ESP8266 board with a HC-SR501 PIR motion sensor and Bosch BME280, humidity, barometric pressure and ambient temperature sensor.
I'm using MicroPython to export the metrics for a [Prometheus](http://prometheus.io/) server to scrape.
Metrics are then graphed using a [Grafana](https://grafana.com/) dashboard.

For more details about the project please have a look at my [blog post](https://www.wtip.net/blog/2020/03/envirosense-esp8266-prometheus-exporter/)

## Requirements
- tested on [MicroPython](https://github.com/micropython/micropython/) v1.12
- I had to use [mpy-cross](https://github.com/micropython/micropython/tree/master/mpy-cross) to precompile the bme280_i2c library

Add a credentials.py file with the following contents:
```
wifi = {'SSID': 'NetworkName', 'pass': 'WifiPassword'}
```

## Attributions
- [uasyncio](https://github.com/micropython/micropython-lib/tree/master/uasyncio)
- [uasyncio.core](https://github.com/micropython/micropython-lib/tree/master/uasyncio.core)
- [bme280_i2c](https://github.com/triplepoint/micropython_bme280_i2c)

**Sample metric output**
```
# HELP wifi_signal_rssi wifi signal rssi
# TYPE wifi_signal_rssi gauge
wifi_signal_rssi -78
# HELP temperature_celsius temperature in celsius from sensor
# TYPE temperature_celsius gauge
temperature_celsius 23.11
# HELP humidity_relative relative humidity percentage from sensor
# TYPE humidity_relative gauge
humidity_relative 33.8945
# HELP pressure_pascal absolute barometric pressure in pascal from sensor
# TYPE pressure_pascal gauge
pressure_pascal 99470
# HELP pir_motion_events PIR motion events
# TYPE pir_motion_events counter
pir_motion_events 443
```

![Assembled EnviroSense in 3D printed enclosure](EnviroSense-assembled-with-enclosure.jpg?raw=true)