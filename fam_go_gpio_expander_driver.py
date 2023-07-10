from pcf8575 import PCF8575

class fam_go_gpio_expander:
    def __init__(self):
        # Setup the address of the GPIO expander
        self.pcf = PCF8575(
            1, 
            0x22)

        # Reset the output, so that its a known state
        self.reset_output()

    def reset_output(self):
        # This does in fact map to everything off
        self.pcf.port = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
        self.port_states =  [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]

    def sync_port_states(self):
        self.pcf.port = self.port_states

    # UHF Power amp controls
    def set_UHF_pwr_amp(self):
        self._set_UHF_pwr_amp_control(True)

    def reset_UHF_pwr_amp(self):
        self._set_UHF_pwr_amp_control(False)

    def _set_UHF_pwr_amp_control(self, on):
        self.port_states[10] = on
        self.sync_port_states()


    # UHF TX/RX switch controls
    def set_UHF_TX(self):
        self._set_UHF_TX_control(True)

    def set_UHF_RX(self):
        self._set_UHF_TX_control(False)

    def _set_UHF_TX_control(self, tx):
        """True is transmit, and false is receive
        """
        self.port_states[11] = tx
        self.sync_port_states()
    
    # BAND SW control
    def set_band_UHF(self):
        self._set_band_sw_control(True)

    def set_band_HF(self):
        self._set_band_sw_control(False)

    def _set_band_sw_control(self, uhf):
        """True sets to UHF, and False set to HF
        """
        self.port_states[12] = uhf
        self.sync_port_states()

    # HF Power amp control
    def set_HF_pwr_amp(self):
        self.reset_HF_tune_amp()
        self._set_HF_pwr_amp_control(True)

    def reset_HF_pwr_amp(self):
        self._set_HF_pwr_amp_control(False)

    def _set_HF_pwr_amp_control(self, on):
        self.port_states[0] = on
        self.sync_port_states()

    # HF TX/RX control 
    def set_HF_TX(self):
        self._set_HF_TX_control(True)

    def set_HF_RX(self):
        self._set_HF_TX_control(False)

    def _set_HF_TX_control(self, tx):
        """True is transmit and false is receive
        """
        self.port_states[1] = not tx
        self.sync_port_states()

    # HF tune amp power control 
    def set_HF_tune_amp(self):
        self.reset_HF_pwr_amp()
        self._set_HF_tune_amp_control(True)

    def reset_HF_tune_amp(self):
        self._set_HF_tune_amp_control(False)

    def _set_HF_tune_amp_control(self, on):
        """Set tune amp control
        """
        self.port_states[2] = on
        self.sync_port_states()
