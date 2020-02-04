# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import gc
gc.collect()
#import webrepl
#webrepl.start()
