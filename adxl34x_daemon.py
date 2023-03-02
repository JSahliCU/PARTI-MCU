import time
import board
import adafruit_adxl34x
import datetime

log_file = 'adxl34x.csv'

i2c = board.I2C()  # uses board.SCL and board.SDA
accelerometer = adafruit_adxl34x.ADXL345(i2c)

with open(log_file, 'a') as f:
    print(str(datetime.datetime.now()) + "UTC, %f, %f, %f"%accelerometer.acceleration, file=f)
# while True:
#     print(str(datetime.datetime.now()) + "UTC, %f, %f, %f"%accelerometer.acceleration,)
#     time.sleep(0.5)