import datetime
import os
import time

import RPi.GPIO as GPIO
import led_mappings

error_log_file = 'error.log'
error_log_file = 'error.log'
error_blink_interval = 1 # seconds

def write_to_log(log_msg):
    with open(error_log_file, 'a') as f:
        print(str(datetime.datetime.now()) + "UTC " + log_msg, file=f)

def throw_error(log_msg):
    write_to_log("ERROR: " + log_msg)

    for bcm_i in led_mappings.led_index_to_bcm_mapping.values():
        GPIO.setup(bcm_i, GPIO.OUT)
        
    while True:
        starttime = time.time()
        for bcm_i in led_mappings.led_index_to_bcm_mapping.values():
            GPIO.output(bcm_i, GPIO.HIGH)
        time.sleep(error_blink_interval - ((time.time() - starttime) % error_blink_interval))
        starttime = time.time()
        for bcm_i in led_mappings.led_index_to_bcm_mapping.values():
            GPIO.output(bcm_i, GPIO.LOW)
        time.sleep(error_blink_interval - ((time.time() - starttime) % error_blink_interval))