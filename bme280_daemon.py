import smbus2
import bme280
import time

port=1
address = 0x76
bus = smbus2.SMBus(port)
log_file = 'bme280.csv'
log_interval = 60

calibration_params = bme280.load_calibration_params(bus, address)

data = bme280.sample(bus, address, calibration_params)
with open(log_file, 'a') as f:
    print("{0},{1:%Y-%m-%d %H:%M:%S.%f%Z},{2:0.3f},{3:0.2f},{4:0.2f}".format(
        data.id, data.timestamp, data.temperature, data.pressure, data.humidity),
        file=f)

