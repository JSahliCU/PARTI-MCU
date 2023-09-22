from run import *

# Initialize light controls
# Set numbering system to broadcom chip numbering scheme
# (as opposed to GPIO.BOARD which would be the header numbering scheme)
GPIO.setmode(GPIO.BCM)

# Setup all of the LED pins as outputs, and off
for bcm_i in led_mappings.led_index_to_bcm_mapping.values():
    GPIO.setup(bcm_i, GPIO.OUT)
    GPIO.output(bcm_i, GPIO.LOW)

# Initialize the state object
sm = state_machine()

# Turn on all the supplies if enable amplifier supplies is set
# UHF Supply
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, GPIO.LOW )

# HF Supply (Disconnected by default)
GPIO.setup(20, GPIO.OUT)
GPIO.output(20, GPIO.LOW)

while True:
    # Update the SM state
    mode = input('Enter transceiver mode, 1 = HF TX, 2 = HF RX, 3 = UHF TX, 4 = UHF RX: ')
    if mode == 'q' or mode == 'quit()':
        break
    mode = int(mode)
    if mode == 1:
        sm.band = 'HF'
        sm.transceiver = 'TX'
    elif mode == 2:
        sm.band = 'HF'
        sm.transceiver = 'RX'
    elif mode == 3:
        sm.band = 'UHF'
        sm.transceiver = 'TX'
    elif mode == 4:
        sm.band = 'UHF'
        sm.transceiver = 'RX'            
    else:
        print('invalid state passed... quitting')
        break
    sm.run_current_state()

sm.fam_go_control.reset_HF_pwr_amp()
sm.fam_go_control.reset_UHF_pwr_amp()

# Kill the currently running GNU instance by sending interrupt
if sm.process is not None:
    if sm.process.poll() is None:
        sm.process.send_signal(signal.SIGINT)
        time.sleep(wait_for_gnu_radio_to_close)

# Can help to power cycle the Hack RF before using it so it comes up in a clean state
# Add this to the install.sh script: 
# sudo apt-get install uhubctl
# Then turn off, wait 5 seconds, then turn on
subprocess.call("echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/unbind", shell=True)
time.sleep(2)
subprocess.call("echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/bind", shell=True)
time.sleep(1)
print('Goodbye')