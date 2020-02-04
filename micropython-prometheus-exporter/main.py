import gc
import uasyncio as asyncio
gc.collect()
import board
import bme280_i2c
import credentials as creds
gc.collect()
board.ap_if.active(False)

HTTP_200_OK = b"""\
HTTP/1.0 200 OK

"""

HTTP_404_NOT_FOUND = b"""\
HTTP/1.0 404 Not Found

Error 404 - Page not found
"""

SENSOR_METRICS = b"""\
# HELP wifi_signal_rssi wifi signal rssi
# TYPE wifi_signal_rssi gauge
wifi_signal_rssi {}
# HELP temperature_celsius temperature in celsius from sensor
# TYPE temperature_celsius gauge
temperature_celsius {}
# HELP humidity_relative relative humidity percentage from sensor
# TYPE humidity_relative gauge
humidity_relative {}
# HELP pressure_pascal absolute barometric pressure in pascal from sensor
# TYPE pressure_pascal gauge
pressure_pascal {}
# HELP pir_motion_events PIR motion events
# TYPE pir_motion_events counter
pir_motion_events {}
"""
pir_counter = 0
temperature = 0
humidity = 0
pressure = 0

async def monitor_wlan():
    was_connected = False
    while True:
        if board.wlan.isconnected():
            if not was_connected:
                print("Monitor: wifi connected!")
                was_connected = True
        else:
            print("Monitor: wifi not connected")
            print("connecting to network...")
            board.wlan.active(True)
            board.wlan.connect(creds.wifi['SSID'], creds.wifi['pass'])
            while not board.wlan.isconnected():
                pass
            print('network config:', board.wlan.ifconfig())
            print('RSSI: ', board.wlan.status('rssi'))
            was_connected = False

        await asyncio.sleep(15)

async def monitor_pir():
    pir_was_active = False
    global pir_counter
    while True:
        if board.pir1() == 1 and pir_was_active == False:
            pir_counter += 1
            print("motion detected #", pir_counter)
            board.led.blue.off()
            pir_was_active = True
        elif board.pir1() == 0:
            pir_was_active = False
            board.led.blue.on()
        await asyncio.sleep_ms(500)

async def monitor_bme280():
    global temperature
    global humidity
    global pressure
    while True:
        sensor = bme280_i2c.BME280_I2C(address=bme280_i2c.BME280_I2C_ADDR_SEC, i2c=board.i2c)
        sensor.set_measurement_settings({
            'filter': bme280_i2c.BME280_FILTER_COEFF_OFF,
            'osr_h': bme280_i2c.BME280_OVERSAMPLING_1X,
            'osr_p': bme280_i2c.BME280_OVERSAMPLING_1X,
            'osr_t': bme280_i2c.BME280_OVERSAMPLING_1X})
        sensor.set_power_mode(bme280_i2c.BME280_FORCED_MODE)
        await asyncio.sleep_ms(40)
        measurement = sensor.get_measurement()
        temperature = measurement.get('temperature')
        humidity = measurement.get('humidity')
        pressure = measurement.get('pressure')
        await asyncio.sleep_ms(5000)

def http_page_metrics(request, writer):
    yield from writer.awrite(HTTP_200_OK)
    rssi =  board.wlan.status('rssi')
    yield from writer.awrite(SENSOR_METRICS.format( rssi, temperature, humidity, pressure, pir_counter))

@asyncio.coroutine
def http_serve(reader, writer):
    try:

        request = (yield from reader.readline())
        print("Request:", request)

        # Read request headers
        while True:
            header = (yield from reader.readline())
            if header == b"" or header == b"\r\n":
                break
            #print(header)

        if request.startswith('GET /metrics'):
            yield from http_page_metrics(request, writer)
        else:
            yield from writer.awrite(HTTP_404_NOT_FOUND)

        yield from writer.aclose()
    finally:
        print("Request: Completed")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(monitor_wlan())
    loop.create_task(monitor_pir())
    loop.create_task(monitor_bme280())
    loop.call_soon(asyncio.start_server(http_serve, "0.0.0.0", 8080))
    loop.run_forever()
    loop.close()