from run import state_machine
import RPi.GPIO as GPIO
import led_mappings

import subprocess
import signal
import time

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

# Turn on 10 V HF Supply (Disconnected by default)
GPIO.setup(20, GPIO.OUT)
GPIO.output(20, GPIO.LOW)

def kill_GNU_instance():
    # Kill the currently running GNU instance by sending interrupt
    if sm.process is not None:
        if sm.process.poll() is None:
            sm.process.send_signal(signal.SIGINT)
            time.sleep(2)

    # Can help to power cycle the Hack RF before using it so it comes up in a clean state
    # Add this to the install.sh script: 
    # sudo apt-get install uhubctl
    # Then turn off, wait 5 seconds, then turn on
    subprocess.call("echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/unbind", shell=True)
    time.sleep(2)
    subprocess.call("echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/bind", shell=True)
    time.sleep(1)

sm.fam_go_control.set_band_HF()
sm.fam_go_control.set_HF_TX()
#if self.tune_enable:
sm.process = subprocess.Popen('exec python HF_TUNE.py', shell=True)
time.sleep(10)

sm.fam_go_control.set_HF_tune_amp()
sm.tuner.tune()
sm.fam_go_control.reset_HF_tune_amp()

kill_GNU_instance()