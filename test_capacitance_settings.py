from run import state_machine
import RPi.GPIO as GPIO
import led_mappings

import subprocess
import signal
import time

GPIO.setwarnings(False)

# Initialize the state object
sm = state_machine(tune_enable=False)

# Initialize light controls
# Set numbering system to broadcom chip numbering scheme
# (as opposed to GPIO.BOARD which would be the header numbering scheme)
GPIO.setmode(GPIO.BCM)

# Setup all of the LED pins as outputs, and off
for bcm_i in led_mappings.led_index_to_bcm_mapping.values():
    GPIO.setup(bcm_i, GPIO.OUT)
    GPIO.output(bcm_i, GPIO.LOW)

# Initialize the heartbeat light
mcu_light_state = False

# Turn off UHF Supply
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, GPIO.HIGH)

# Turn off 10 V HF Supply (Disconnected by default)
GPIO.setup(20, GPIO.OUT)
GPIO.output(20, GPIO.HIGH)

while True:
    cap_solid = input('Solid capacitance: ')
    cap_split = input('Split capacitance: ')
    
    if cap_solid == 'q' or cap_split == 'q':
        break

    if not cap_solid == '':
        sm.tuner.tb_solid.set_capacitance(int(cap_solid))
    
    if not cap_split == '':
        sm.tuner.tb_split.set_capacitance(int(cap_split))

    print('ACK')