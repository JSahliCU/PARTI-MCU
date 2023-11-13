import RPi.GPIO as GPIO
import led_mappings
from pcf8575 import PCF8575
import time
from ADCPi import ADCPi
import datetime

from error_log import write_to_log, throw_error

def convert_bool_array_to_int(bool_array, big_endian=True, weights=None):
    if weights is not None:
        return sum(weights[i]*b for i, b in enumerate(bool_array))
    elif big_endian:
        return sum(2**i*b for i, b in enumerate(reversed(bool_array)))
    else:
        return sum(2**i*b for i, b in enumerate(bool_array))

def convert_int_to_bool_array(n, format_string='07b'):
    return [bool(int(digit)) for digit in format(n, format_string)]

class tuning_bank:
    def reset_output(self):
        self.port_states =  [True, True, True, True, 
                             True, True, True, True, 
                             True, True, True, True, 
                             True, True, True, True, ]
        self.sync_port_states()

    def sync_port_states(self):
        self.pcf.port = list(reversed(self.port_states))
        time.sleep(0.1)

    def reset_capacitance(self):
        for i, r in enumerate(self.relays):
            self.port_states[r.reset_pin] = False
        
        self.sync_port_states()
        self.reset_output()

        self.current_capacitance_pF = 0
        self.bank_state = 127

    class relay:
        def __init__(self, set_pin, reset_pin, cap_value):
            self.set_pin = set_pin
            self.reset_pin = reset_pin
            self.cap_value = cap_value

    def set_capacitance(self, cap_pF, debug=False):
        """Set the bank capacitance to the passed value. 
        Calculates the minimum number of relays to change from the current state to the intended state

        :param cap_pF: Capacitance to set the bank to in pF. The range is 0 pF to 78 pF in 1 pF steps.
        :type cap_pF: float
        :return: The difference between the set capacitance and the desired capacitance (set - desired)
        :rtype: float
        """
        # Map which relays should be set to give the desired value
        self.attempted_set_value = cap_pF
        future_bank_state_ba = convert_int_to_bool_array(0)
        for i, r in enumerate(self.relays):
            cap_value = r.cap_value
            if cap_pF >= cap_value:
                if debug:
                    print('s')
                future_bank_state_ba[i] = False
                #self.port_states[self.set_caps[cap_value]] = True
                cap_pF -= cap_value
            else:
                if debug:
                    print ('r')
                future_bank_state_ba[i] = True

        # Figure out how to change the bank from the current value 
        # to that future value with the minimum number of relay changes
        future_bank_state = convert_bool_array_to_int(future_bank_state_ba)
        set_caps_bool_array = convert_int_to_bool_array(future_bank_state \
            & (self.bank_state ^ future_bank_state))
        reset_caps_bool_array = convert_int_to_bool_array(~future_bank_state \
            & (self.bank_state ^ future_bank_state))

        # Set the correct pins on the PCF8575
        for i, r in enumerate(self.relays):
            self.port_states[r.set_pin] = set_caps_bool_array[i]
            self.port_states[r.reset_pin] = reset_caps_bool_array[i]

        self.sync_port_states()
        self.reset_output()

        # Store the set capacitance
        self.current_capacitance_pF = self.attempted_set_value - cap_pF
        if debug:
            print(self.bank_state)
        self.bank_state = future_bank_state
        if debug:
            print(future_bank_state)

        
        # Return the remainder
        return cap_pF

class tuning_bank_solid(tuning_bank):
    def __init__(self):
        # Setup the address of the GPIO expander
        self.pcf = PCF8575(
            0,
            0x20) # U3

        # Reset the output, so that its a known state
        self.reset_output()

        self.relays = [
            tuning_bank.relay(2, 3, 39),
            tuning_bank.relay(4, 5, 20),
            tuning_bank.relay(6, 7, 10),
            # tuning_bank.relay(10, 11, 5),
            # tuning_bank.relay(12, 13, 2),
            # tuning_bank.relay(14, 15, 1),
            # tuning_bank.relay(16, 17, 1),
            tuning_bank.relay(8, 9, 5),
            tuning_bank.relay(10, 11, 2),
            tuning_bank.relay(12, 13, 1),
            tuning_bank.relay(14, 15, 1),
        ]
        self.relays.sort(key=lambda x: x.cap_value, reverse=True)
        
        # reset the capacitor banks to 0 pF
        self.reset_capacitance()

class tuning_bank_split(tuning_bank):
    def __init__(self):
        # Setup the address of the GPIO expander
        self.pcf = PCF8575(
            0,
            0x27) # U4

        # Reset the output, so that its a known state
        self.reset_output()

        self.relays = [
            tuning_bank.relay(2, 3, 1),
            tuning_bank.relay(4, 5, 1),
            tuning_bank.relay(6, 7, 2),
            # tuning_bank.relay(10, 11, 5),
            # tuning_bank.relay(12, 13, 10),
            # tuning_bank.relay(14, 15, 20),
            # tuning_bank.relay(16, 17, 39),
            tuning_bank.relay(8, 9, 5),
            tuning_bank.relay(10, 11, 10),
            tuning_bank.relay(12, 13, 20),
            tuning_bank.relay(14, 15, 39),
        ]
        self.relays.sort(key=lambda x: x.cap_value, reverse=True)
        
        # reset the capacitor banks to 0 pF
        self.reset_capacitance()

SOLID_LED = led_mappings.led_to_bcm_mapping.HF_L1_SOLID
SPLIT_LED = led_mappings.led_to_bcm_mapping.HF_L2_SPLIT

NUMBER_OF_AVERAGES = 1

class tuner():
    def __init__(self):
        # Setup the tuning banks
        self.tb_split = tuning_bank_split()
        self.tb_solid = tuning_bank_solid()

        with open('split_tune.txt', 'r') as f:
            self.tb_split.set_capacitance(int(f.read()))

        with open('solid_tune.txt', 'r') as f:
            self.tb_solid.set_capacitance(int(f.read()))

        # Setup the ADC used for tuning
        self.adc = ADCPi(0x68, 0x68, 18, 0) # TODO check bus setting
        self.adc.set_conversion_mode(0) 

    def read_voltage_solid(self):
        ret_val = 0
        for i in range(NUMBER_OF_AVERAGES):
            ret_val += self.adc.read_raw(1)
        return ret_val / NUMBER_OF_AVERAGES

    def read_voltage_split(self):
        ret_val = 0
        for i in range(NUMBER_OF_AVERAGES):
            ret_val += self.adc.read_raw(2)
        return ret_val / NUMBER_OF_AVERAGES

    def wait_for_adc_settle_time(self):
        time.sleep(0.050)

    def tune(self):
        # Turn off the tuning LEDs while tuning
        GPIO.output(SOLID_LED, GPIO.LOW)
        GPIO.output(SPLIT_LED, GPIO.LOW)

        light_state = False
        
        # Read from both ADCs, try moving up in capacitance and down on 
        # each individually, then both same direction, both opposite directions
        # and see if any direction decreases the voltage read, repeat 20 times

        write_to_log('Tuning HF system')
        for i in range(20):
            # Check voltage at current state
            nominal_capacitance_solid = self.tb_solid.current_capacitance_pF
            nominal_capacitance_split = self.tb_split.current_capacitance_pF

            # Check voltage in all directions
            test_settings = [
                # so, sp, vo
                (nominal_capacitance_solid, nominal_capacitance_split),
                (nominal_capacitance_solid+1, nominal_capacitance_split),
                (nominal_capacitance_solid, nominal_capacitance_split+1),
                (nominal_capacitance_solid-1, nominal_capacitance_split),
                (nominal_capacitance_solid, nominal_capacitance_split-1),
                (nominal_capacitance_solid+1, nominal_capacitance_split+1),
                (nominal_capacitance_solid+1, nominal_capacitance_split-1),
                (nominal_capacitance_solid-1, nominal_capacitance_split+1),
                (nominal_capacitance_solid-1, nominal_capacitance_split-1),
            ]

            test_results = []

            for so, sp in test_settings:
                self.tb_solid.set_capacitance(so) # Log if returns value that is not 0
                self.tb_split.set_capacitance(sp) # Log if returns value that is not 0
                self.wait_for_adc_settle_time()
                adc_read_val = self.read_voltage_solid() + self.read_voltage_split()
                test_results.append((so, sp, adc_read_val))

            test_results.sort(key=lambda tup: tup[2])  # sort the values in ascending order of adc read val

            new_cap_solid = test_results[0][0]
            new_cap_split = test_results[0][1]
            min_volt_found = test_results[0][2]

            self.tb_solid.set_capacitance(new_cap_solid) # Log if returns value that is not 0
            self.tb_split.set_capacitance(new_cap_split) # Log if returns value that is not 0

            # Update the heartbeat file
            with open('heartbeat.txt', 'w') as f:
                print(str(datetime.datetime.now()), file=f)

            # Log the capacitance value to the error file, just in case there some
            write_to_log(str(new_cap_solid) +','+ str(new_cap_split) + ',' + str(min_volt_found))

            light_state = not light_state
            if light_state:
                GPIO.output(SOLID_LED, GPIO.HIGH)
                GPIO.output(SPLIT_LED, GPIO.HIGH)
            else:
                GPIO.output(SOLID_LED, GPIO.LOW)
                GPIO.output(SPLIT_LED, GPIO.LOW)         

        # Turn the Tuning LEDs to tuned
        GPIO.output(SOLID_LED, GPIO.HIGH)
        GPIO.output(SPLIT_LED, GPIO.HIGH)