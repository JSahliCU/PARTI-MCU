from pcf8575 import PCF8575
import time

i2c_port_num = 0
pcf_address = 0x20

pcf = PCF8575(i2c_port_num, pcf_address)

print(pcf.port)

pcf.port = [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]

print (pcf.port)
time.sleep(10)

pcf.port = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]

print (pcf.port)