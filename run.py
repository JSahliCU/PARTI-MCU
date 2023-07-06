import time
import datetime
import RPi.GPIO as GPIO
import led_mappings
import tuning_banks

heartbeat_interval = 30

error_log_file = 'error.log'
error_blink_interval = 1

class state_machine:
    def __init__(self):
        # Transeiver states
        # Always boot to UHF first
        self.band = 'UHF'
        # Check if RX/TX device and set for boot state
        with open('boot.txt', 'r') as f:
            if f.read() == 'RX':
                self.transceiver = 'RX'
            elif f.read() == 'TX':
                self.transceiver = 'TX'
            else:
                throw_error('boot.txt file contains invalid state')

        self.boot_transceiver = self.transceiver

        self.record_band_and_transceiver()

        # Light states
        self.MCU_ON_state = None
        self.HF_L1_SOLID_state = None
        self.HF_L2_SPLIT_state = None
        self.HF_TX_state = None
        self.HF_RX_state = None
        self.UHF_TX_state = None
        self.UHF_RX_state = None
        
        # Stored timings
        self.last_sm_update_time = None
        self.last_HF_tune_time = None 

        # Stored intervals
        with open('transceiver_state_interval.txt', 'r') as f:
            self.sm_update_interval = int(f.read()) 

        with open('tune_interval.txt', 'r') as f:
            self.hf_tune_interval = int(f.read()) 

    def __str__(self):
        return self.band + ', ' + self.transceiver

    def record_band_and_transceiver(self):
        with open('band.txt') as f:
            print(self.band, file=f)

        with open('RX_TX.txt') as f:
            print(self.transceiver, file=f)

    def next(self):
        if self.transceiver != self.boot_transceiver:
            self.toggle_band()

        self.toggle_transceiver()

        self.record_band_and_transceiver()

    def toggle_transceiver(self):
        if self.transceiver == 'RX':
            self.transceiver = 'TX'
        else # self.transeiver == 'TX':
            self.transceiver = 'RX'

    def toggle_band(self):
        if self.band == 'UHF':
            self.band = 'HF'
        else # self.band == 'HF':
            self.band = 'UHF'

    def run_current_state(self):
        # Reset all of the state lights
        GPIO.output(led_mappings.led_to_bcm_mapping.UHF_RX, GPIO.LOW)
        GPIO.output(led_mappings.led_to_bcm_mapping.UHF_TX, GPIO.LOW)
        GPIO.output(led_mappings.led_to_bcm_mapping.HF_RX, GPIO.LOW)
        GPIO.output(led_mappings.led_to_bcm_mapping.HF_TX, GPIO.LOW)

        # Write the gpios on the expanders for each state
        # TODO

        if self.band == 'UHF':
            if self.transceiver == 'RX':
                GPIO.output(led_mappings.led_to_bcm_mapping.UHF_RX, GPIO.HIGH)
                # BOOT A GNU RADIO INSTANCE TODO
            else # self.transceiver == 'TX'
                GPIO.output(led_mappings.led_to_bcm_mapping.UHF_TX, GPIO.HIGH)
                # BOOT A GNU RADIO INSTANCE TODO
        else #self.band == 'HF':
            if self.transceiver == 'RX':
                GPIO.output(led_mappings.led_to_bcm_mapping.HF_RX, GPIO.HIGH)
                # BOOT A GNU RADIO INSTANCE TODO
            else # self.transceiver == 'TX'
                GPIO.output(led_mappings.led_to_bcm_mapping.HF_TX, GPIO.HIGH)
                # BOOT A GNU RADIO INSTANCE TODO

def write_to_log(log_msg):
    with open(error_log_file, 'a') as f:
        print(str(datetime.datetime.now()) + "UTC " + log_msg, file=f)

def throw_error(log_msg):
    write_to_log("ERROR: " + log_msg)

    while True:
        starttime = time.time()
        while True:
            for bcm_i in led_mappings.led_index_to_bcm_mapping.values():
                GPIO.output(bcm_i, GPIO.HIGH)
            time.sleep(error_blink_interval - ((time.time() - starttime) % error_blink_interval))
            for bcm_i in led_mappings.led_index_to_bcm_mapping.values():
                GPIO.output(bcm_i, GPIO.LOW)
            time.sleep(error_blink_interval - ((time.time() - starttime) % error_blink_interval))

def main():
    # Init
    write_to_log('Initializing')

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
    sm.mcu_light_state = False

    # Initially tune the HF state
    tuning_banks.tune_HF()
    starttime = time.time()
    sm.last_HF_tune_time = starttime

    # Start the initial state
    sm.run_current_state()  

    # Begin the main loop
    sm.last_sm_update_time = starttime
    write_to_log('Beginning main loop')
    write_to_log(str(sm))

    # Main loop
    while True:
        starttime = time.time()
        with open('heartbeat.txt') as f:
            print(str(datetime.datetime.now()), file=f)

        # Blink the MCU light
        if sm.mcu_light_state:
            GPIO.output(led_mappings.led_to_bcm_mapping.MCU_ON, GPIO.LOW)
            sm.mcu_light_state = False
        else:
            GPIO.output(led_mappings.led_to_bcm_mapping.MCU_ON, GPIO.HIGH)
            sm.mcu_light_state = True
        
        # Do everything
        # Update the SM state
        if (time.time() - sm.last_sm_update_time) > sm.hf_tune_interval:
            sm.next()
            sm.run_current_state()
            sm.last_sm_update_time = time.time()

        # Tune the receiver if necessary
        if sm.band == 'HF' and (time.time() - sm.last_HF_tune_time) > sm.sm_update_interval:
            tuning_banks.tune_HF()
            sm.last_HF_tune_time = time.time()

        # Log machine state
        write_to_log(str(sm))
        time.sleep(heartbeat_interval - ((time.time() - starttime) % heartbeat_interval))

if __name__ == "__main__":
    main()