import machine

class led:
    blue = machine.Pin(2, machine.Pin.OUT)

led.blue.off()
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
pir1 = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)

import network
wlan = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)