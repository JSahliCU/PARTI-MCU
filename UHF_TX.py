#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: UHF TX
# Author: Jake Sahli
# GNU Radio version: 3.8.2.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import blocks
import pmt
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import osmosdr
import time

from gnuradio import qtgui

class UHF_TX(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "UHF TX")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("UHF TX")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "UHF_TX")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.bps = bps = 1e3
        self.samp_rate = samp_rate = (int) (2e6)
        self.packet_bits = packet_bits = 108
        self.header_bits = header_bits = 8
        self.delta_f = delta_f = 1.1 * bps
        self.baud_rate = baud_rate = 1000
        self.M = M = 2
        self.samp_per_symbol = samp_per_symbol = (int)(samp_rate * (1 / baud_rate))
        self.samp_per_bit = samp_per_bit = (int)(samp_rate * (1 / bps))
        self.rf_gain = rf_gain = 14
        self.payload_bits = payload_bits = packet_bits - header_bits
        self.if_gain = if_gain = 28
        self.freq = freq = 413e6
        self.demod_offset = demod_offset = 1e3
        self.bb_gain = bb_gain = 20
        self.bandwidth = bandwidth = M * delta_f

        ##################################################
        # Blocks
        ##################################################
        self._rf_gain_range = Range(0, 14, 1, 14, 200)
        self._rf_gain_win = RangeWidget(self._rf_gain_range, self.set_rf_gain, 'rf_gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._rf_gain_win)
        self._if_gain_range = Range(0, 28, 1, 28, 200)
        self._if_gain_win = RangeWidget(self._if_gain_range, self.set_if_gain, 'if_gain', "counter_slider", float)
        self.top_grid_layout.addWidget(self._if_gain_win)
        # Create the options list
        self._baud_rate_options = (1000, 10000, 100000, )
        # Create the labels list
        self._baud_rate_labels = ('1 kbps', '10 kbps', '100 kbps', )
        # Create the combo box
        # Create the radio buttons
        self._baud_rate_group_box = Qt.QGroupBox('Symbol Rate' + ": ")
        self._baud_rate_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._baud_rate_button_group = variable_chooser_button_group()
        self._baud_rate_group_box.setLayout(self._baud_rate_box)
        for i, _label in enumerate(self._baud_rate_labels):
            radio_button = Qt.QRadioButton(_label)
            self._baud_rate_box.addWidget(radio_button)
            self._baud_rate_button_group.addButton(radio_button, i)
        self._baud_rate_callback = lambda i: Qt.QMetaObject.invokeMethod(self._baud_rate_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._baud_rate_options.index(i)))
        self._baud_rate_callback(self.baud_rate)
        self._baud_rate_button_group.buttonClicked[int].connect(
            lambda i: self.set_baud_rate(self._baud_rate_options[i]))
        self.top_grid_layout.addWidget(self._baud_rate_group_box)
        self.osmosdr_sink_0 = osmosdr.sink(
            args="numchan=" + str(1) + " " + "hackrf=0"
        )
        self.osmosdr_sink_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_sink_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0.set_center_freq(freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(rf_gain, 0)
        self.osmosdr_sink_0.set_if_gain(if_gain, 0)
        self.osmosdr_sink_0.set_bb_gain(bb_gain, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(demod_offset*2 + delta_f * 10, 0)
        self.blocks_vco_c_0_0 = blocks.vco_c(samp_rate, (delta_f) * 2 * 3.14159, 1)
        self.blocks_uchar_to_float_1 = blocks.uchar_to_float()
        self.blocks_repeat_0_0 = blocks.repeat(gr.sizeof_char*1, (int)(samp_rate * (1 / baud_rate)))
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/tbbg/tx_data', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_add_const_vxx_0_0 = blocks.add_const_ff(demod_offset / delta_f)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_const_vxx_0_0, 0), (self.blocks_vco_c_0_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.blocks_repeat_0_0, 0))
        self.connect((self.blocks_repeat_0_0, 0), (self.blocks_uchar_to_float_1, 0))
        self.connect((self.blocks_uchar_to_float_1, 0), (self.blocks_add_const_vxx_0_0, 0))
        self.connect((self.blocks_vco_c_0_0, 0), (self.osmosdr_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "UHF_TX")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_bps(self):
        return self.bps

    def set_bps(self, bps):
        self.bps = bps
        self.set_delta_f(1.1 * self.bps)
        self.set_samp_per_bit((int)(self.samp_rate * (1 / self.bps)))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samp_per_bit((int)(self.samp_rate * (1 / self.bps)))
        self.set_samp_per_symbol((int)(self.samp_rate * (1 / self.baud_rate)))
        self.blocks_repeat_0_0.set_interpolation((int)(self.samp_rate * (1 / self.baud_rate)))
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate)

    def get_packet_bits(self):
        return self.packet_bits

    def set_packet_bits(self, packet_bits):
        self.packet_bits = packet_bits
        self.set_payload_bits(self.packet_bits - self.header_bits)

    def get_header_bits(self):
        return self.header_bits

    def set_header_bits(self, header_bits):
        self.header_bits = header_bits
        self.set_payload_bits(self.packet_bits - self.header_bits)

    def get_delta_f(self):
        return self.delta_f

    def set_delta_f(self, delta_f):
        self.delta_f = delta_f
        self.set_bandwidth(self.M * self.delta_f)
        self.blocks_add_const_vxx_0_0.set_k(self.demod_offset / self.delta_f)
        self.osmosdr_sink_0.set_bandwidth(self.demod_offset*2 + self.delta_f * 10, 0)

    def get_baud_rate(self):
        return self.baud_rate

    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate
        self._baud_rate_callback(self.baud_rate)
        self.set_samp_per_symbol((int)(self.samp_rate * (1 / self.baud_rate)))
        self.blocks_repeat_0_0.set_interpolation((int)(self.samp_rate * (1 / self.baud_rate)))

    def get_M(self):
        return self.M

    def set_M(self, M):
        self.M = M
        self.set_bandwidth(self.M * self.delta_f)

    def get_samp_per_symbol(self):
        return self.samp_per_symbol

    def set_samp_per_symbol(self, samp_per_symbol):
        self.samp_per_symbol = samp_per_symbol

    def get_samp_per_bit(self):
        return self.samp_per_bit

    def set_samp_per_bit(self, samp_per_bit):
        self.samp_per_bit = samp_per_bit

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.osmosdr_sink_0.set_gain(self.rf_gain, 0)

    def get_payload_bits(self):
        return self.payload_bits

    def set_payload_bits(self, payload_bits):
        self.payload_bits = payload_bits

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self.osmosdr_sink_0.set_if_gain(self.if_gain, 0)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_sink_0.set_center_freq(self.freq, 0)

    def get_demod_offset(self):
        return self.demod_offset

    def set_demod_offset(self, demod_offset):
        self.demod_offset = demod_offset
        self.blocks_add_const_vxx_0_0.set_k(self.demod_offset / self.delta_f)
        self.osmosdr_sink_0.set_bandwidth(self.demod_offset*2 + self.delta_f * 10, 0)

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain
        self.osmosdr_sink_0.set_bb_gain(self.bb_gain, 0)

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth





def main(top_block_cls=UHF_TX, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
