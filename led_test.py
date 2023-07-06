import RPi.GPIO as GPIO
import time
import led_mappings

# Set numbering system to broadcom chip numbering scheme
# (as opposed to GPIO.BOARD which would be the header numbering scheme)
GPIO.setmode(GPIO.BCM)

# Setup all of the LED pins as outputs
for bcm_i in led_mappings.led_index_to_bcm_mapping.values():
    GPIO.setup(bcm_i, GPIO.OUT)
    GPIO.output(bcm_i, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(bcm_i, GPIO.LOW)

GPIO.cleanup()