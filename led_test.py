import RPi.GPIO as GPIO
import time
import enum

# WARNING
# This script was written for interface pcb v1a1a

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

led_index_to_bcm_mapping ={
     1: 17,
     2: 27,
     3: 22,
     4: 5,
     5: 6,
     6: 13,
     7: 19
     }

led_to_bcm_mapping = enum(
    HF_L1_SOLID = led_index_to_bcm_mapping[1],
    HF_L2_SPLIT = led_index_to_bcm_mapping[2],
    HF_TX = led_index_to_bcm_mapping[3],
    HF_RX = led_index_to_bcm_mapping[4],
    UHF_TX = led_index_to_bcm_mapping[5],
    UHF_RX = led_index_to_bcm_mapping[6],
    MCU_ON = led_index_to_bcm_mapping[7],
    #MAIN_DISCO = led_index_to_bcm_mapping[8], # Main disconnect has no led on the interface v1a1a
)

# Set numbering system to broadcom chip numbering scheme
# (as opposed to GPIO.BOARD which would be the header numbering scheme)
GPIO.setmode(GPIO.BCM)

# Setup all of the LED pins as outputs
for bcm_i in led_index_to_bcm_mapping.values():
    GPIO.setup(bcm_i, GPIO.OUT)
    GPIO.output(bcm_i, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(bcm_i, GPIO.LOW)

GPIO.cleanup()