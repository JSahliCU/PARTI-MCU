from pcf8575 import PCF8575
import time
from error_log import write_to_log, throw_error

class fam_go_gpio_expander:
    def __init__(self):
        # Setup the address of the GPIO expander
        self.pcf = PCF8575(
            0, 
            0x22)

        # Reset the output, so that its a known state
        self.reset_output()

    def reset_output(self):
        self.port_states =  [True, True, True, True, 
                             True, True, True, True, 
                             True, True, True, True, 
                             True, True, True, True]
        self.sync_port_states()

    def sync_port_states(self):
        self.pcf.port = list(reversed(self.port_states))
        time.sleep(0.1)

    # UHF Power amp controls
    def set_UHF_pwr_amp(self):
        self._set_UHF_pwr_amp_control(False)

    def reset_UHF_pwr_amp(self):
        self._set_UHF_pwr_amp_control(True)

    def _set_UHF_pwr_amp_control(self, on):
        self.port_states[8] = on
        self.sync_port_states()


    # UHF TX/RX switch controls
    def set_UHF_TX(self):
        self._set_UHF_TX_control(False)

    def set_UHF_RX(self):
        self._set_UHF_TX_control(True)

    def _set_UHF_TX_control(self, tx):
        """False is transmit, and True is receive
        """
        self.port_states[9] = tx
        self.sync_port_states()
    
    # BAND SW control
    def set_band_UHF(self):
        self._set_band_sw_control(False)

    def set_band_HF(self):
        self._set_band_sw_control(True)

    def _set_band_sw_control(self, uhf):
        """True sets to HF, and False set to UHF
        """
        self.port_states[10] = uhf
        self.sync_port_states()

    # HF Power amp control
    def set_HF_pwr_amp(self):
        self.reset_HF_tune_amp()
        try: # Occasionally this sequence will throw an OS Error for no discernable reason, even though the command still works
            self._set_HF_pwr_amp_control(False)
        except(OSError) as e:
            write_to_log('OSError 121 caught during set_HF_pwr_amp')

    def reset_HF_pwr_amp(self):
        self._set_HF_pwr_amp_control(True)

    def _set_HF_pwr_amp_control(self, on):
        self.port_states[0] = on
        self.sync_port_states()

    # HF TX/RX control 
    def set_HF_TX(self):
        self._set_HF_TX_control(False)

    def set_HF_RX(self):
        self._set_HF_TX_control(True)

    def _set_HF_TX_control(self, tx):
        """False is transmit and True is receive
        """
        self.port_states[1] = not tx
        self.sync_port_states()

    # HF tune amp power control 
    def set_HF_tune_amp(self):
        self.reset_HF_pwr_amp()
        self._set_HF_tune_amp_control(False)

    def reset_HF_tune_amp(self):
        self._set_HF_tune_amp_control(True)

    def _set_HF_tune_amp_control(self, on):
        """Set tune amp control
        """
        self.port_states[2] = on
        self.sync_port_states()
