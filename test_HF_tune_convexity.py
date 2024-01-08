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

search_range = int(input('Enter tuning capacitance range: '))
print(f'Nominal solid value: {0}'.format(sm.tuner.tb_solid.current_capacitance_pF))
print(f'Nominal split value: {0}'.format(sm.tuner.tb_split.current_capacitance_pF))
nominal_capacitance_solid = int(input('Enter starting solid loop capacitance'))
nominal_capacitance_split = int(input('Enter starting split loop capacitance'))

sm.fam_go_control.set_HF_pwr_amp()

with open('HF_tune_convexity.csv', 'w') as f:
    print('Amplifier Voltage, Solid Capacitance, Split Capacitance, \
            Immediate Reading Solid, Immediate Reading Split, Immediate Reading Combined,', \
            file=f)
 
    for solid_cap in range(nominal_capacitance_solid - search_range, nominal_capacitance_solid + search_range + 1):
        for split_cap in range(nominal_capacitance_split - search_range, nominal_capacitance_split + search_range + 1):
            
            sm.tuner.tb_solid.set_capacitance(solid_cap)
            sm.tuner.tb_split.set_capacitance(split_cap)

            immediate_reading_solid = sm.tuner.read_voltage_solid()
            immediate_reading_split = sm.tuner.read_voltage_split()
            
            print('Solid voltage read {0}, with cap = {1}'.format(immediate_reading_solid, sm.tuner.tb_solid.current_capacitance_pF))
            print('Split voltage read {0}, with cap = {1}'.format(immediate_reading_split, sm.tuner.tb_split.current_capacitance_pF))

            print('10, {0}, {1}, \
                {2}, {3}, {4}'.format(
                    solid_cap, split_cap,
                    immediate_reading_solid, immediate_reading_split, immediate_reading_solid + immediate_reading_split
                ), file=f)
            
            input('Press Enter once you have saved the measurement')

sm.fam_go_control.reset_HF_pwr_amp()

kill_GNU_instance()

# Turn off UHF Supply
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, GPIO.HIGH)

# Turn off 10 V HF Supply
GPIO.setup(20, GPIO.OUT)
GPIO.output(20, GPIO.HIGH)