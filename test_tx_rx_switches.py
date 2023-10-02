from run import state_machine
import RPi.GPIO as GPIO
import led_mappings

# Initialize the state object
sm = state_machine()

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

# Turn on all the supplies, just in case they are off
# UHF Supply
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, GPIO.LOW)

# HF Supply (Disconnected by default)
GPIO.setup(20, GPIO.OUT)
GPIO.output(20, GPIO.LOW)

# No need to set the 5.1 V enable, because HiZ is on, and the default state of the GPIO pin is HiZ

# Start the initial state
sm.run_current_state()  

while True:
    input('Current state = ' + sm.band + ' ' + sm.transceiver + '. Press Enter to change state.')
    sm.next()
    sm.run_current_state()