#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: UHF RX
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
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
import epy_block_0
import osmosdr
import time

from gnuradio import qtgui

class UHF_RX(gr.top_block, Qt.QWidget):

    def __init__(self, center_frequency_offset_error=0.5):
        gr.top_block.__init__(self, "UHF RX")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("UHF RX")
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

        self.settings = Qt.QSettings("GNU Radio", "UHF_RX")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.center_frequency_offset_error = center_frequency_offset_error

        ##################################################
        # Variables
        ##################################################
        self.bps = bps = 1e3
        self.M = M = 2
        self.samp_rate = samp_rate = (int) (5e5)
        self.baud_rate = baud_rate = bps * 2 / M
        self.samp_per_symbol = samp_per_symbol = samp_rate * (1 / baud_rate)
        self.rf_gain = rf_gain = 0
        self.packet_bits = packet_bits = 108
        self.if_gain = if_gain = 16
        self.header_bits = header_bits = 8
        self.freq = freq = 413e6
        self.delta_f = delta_f = 1.1 * bps
        self.bb_gain = bb_gain = 16
        self.samp_per_symbol_display = samp_per_symbol_display = samp_per_symbol
        self.samp_per_bit = samp_per_bit = (int)(samp_rate * (1 / bps))
        self.rf_gain_display = rf_gain_display = rf_gain
        self.payload_bits = payload_bits = packet_bits - header_bits
        self.if_gain_display = if_gain_display = if_gain
        self.freq_display = freq_display = freq
        self.freq_0 = freq_0 = 413e6
        self.demod_offset = demod_offset = 1e3
        self.bb_gain_display = bb_gain_display = bb_gain
        self.baud_rate_display = baud_rate_display = baud_rate
        self.baud_rate_0 = baud_rate_0 = bps * 2 / M
        self.bandwidth = bandwidth = M * delta_f
        self.agc_integration_const = agc_integration_const = 2e5

        ##################################################
        # Blocks
        ##################################################
        self._samp_per_symbol_display_tool_bar = Qt.QToolBar(self)

        if None:
            self._samp_per_symbol_display_formatter = None
        else:
            self._samp_per_symbol_display_formatter = lambda x: eng_notation.num_to_str(x)

        self._samp_per_symbol_display_tool_bar.addWidget(Qt.QLabel('samp_per_symbol_display' + ": "))
        self._samp_per_symbol_display_label = Qt.QLabel(str(self._samp_per_symbol_display_formatter(self.samp_per_symbol_display)))
        self._samp_per_symbol_display_tool_bar.addWidget(self._samp_per_symbol_display_label)
        self.top_grid_layout.addWidget(self._samp_per_symbol_display_tool_bar)
        self.root_raised_cosine_filter_0 = filter.fir_filter_fff(
            1,
            firdes.root_raised_cosine(
                1,
                samp_rate,
                baud_rate,
                0.35,
                (int) (1e3)))
        self._rf_gain_display_tool_bar = Qt.QToolBar(self)

        if None:
            self._rf_gain_display_formatter = None
        else:
            self._rf_gain_display_formatter = lambda x: str(x)

        self._rf_gain_display_tool_bar.addWidget(Qt.QLabel('rf_gain_display' + ": "))
        self._rf_gain_display_label = Qt.QLabel(str(self._rf_gain_display_formatter(self.rf_gain_display)))
        self._rf_gain_display_tool_bar.addWidget(self._rf_gain_display_label)
        self.top_grid_layout.addWidget(self._rf_gain_display_tool_bar)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
            (int) (10 * samp_rate / baud_rate), #size
            samp_rate , #samp_rate
            "", #name
            3 #number of inputs
        )
        self.qtgui_time_sink_x_0_0.set_update_time(1)
        self.qtgui_time_sink_x_0_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(False)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


        labels = ['I', 'FM Demod', 'Q', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'dark blue', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(3):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            100 * 10, #size
            10 * samp_rate / baud_rate, #samp_rate
            "", #name
            3 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(1)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 2)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(3):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + "hackrf=0"
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(True, 0)
        self.osmosdr_source_0.set_gain(rf_gain, 0)
        self.osmosdr_source_0.set_if_gain(if_gain, 0)
        self.osmosdr_source_0.set_bb_gain(bb_gain, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(bandwidth * 10 + demod_offset * 2, 0)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                10e3,
                3e3,
                firdes.WIN_HAMMING,
                6.76))
        self._if_gain_display_tool_bar = Qt.QToolBar(self)

        if None:
            self._if_gain_display_formatter = None
        else:
            self._if_gain_display_formatter = lambda x: str(x)

        self._if_gain_display_tool_bar.addWidget(Qt.QLabel('if_gain_display' + ": "))
        self._if_gain_display_label = Qt.QLabel(str(self._if_gain_display_formatter(self.if_gain_display)))
        self._if_gain_display_tool_bar.addWidget(self._if_gain_display_label)
        self.top_grid_layout.addWidget(self._if_gain_display_tool_bar)
        self._freq_display_tool_bar = Qt.QToolBar(self)

        if None:
            self._freq_display_formatter = None
        else:
            self._freq_display_formatter = lambda x: eng_notation.num_to_str(x)

        self._freq_display_tool_bar.addWidget(Qt.QLabel('freq_display' + ": "))
        self._freq_display_label = Qt.QLabel(str(self._freq_display_formatter(self.freq_display)))
        self._freq_display_tool_bar.addWidget(self._freq_display_label)
        self.top_grid_layout.addWidget(self._freq_display_tool_bar)
        self.epy_block_0 = epy_block_0.blk(max_input_level=0.75, min_input_level=0.1, update_period=0.5, delay_between_settings=0.25, auto_log_time_min=15, ratio_of_freq_change_to_diff=0.1, freq_offset_limit=15e3, callback_rf_gain=self.set_rf_gain, callback_if_gain=self.set_if_gain, callback_bb_gain=self.set_bb_gain, symbol_delta_f=delta_f, demod_offset=demod_offset, callback_set_freq=self.set_freq, callback_get_freq_0=self.get_freq_0, callback_get_freq=self.get_freq, callback_set_symbol_rate=self.set_baud_rate, callback_get_symbol_rate_0=self.get_baud_rate_0)
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_ff(
            digital.TED_SIGNAL_TIMES_SLOPE_ML,
            samp_per_symbol,
            0.045,
            1.0,
            1.0,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_repeat_0_0_1 = blocks.repeat(gr.sizeof_float*1, 10)
        self.blocks_repeat_0_0_0 = blocks.repeat(gr.sizeof_float*1, 10)
        self.blocks_repeat_0_0 = blocks.repeat(gr.sizeof_float*1, 10)
        self.blocks_multiply_const_vxx_1_0_0_0 = blocks.multiply_const_ff(1/(agc_integration_const))
        self.blocks_multiply_const_vxx_1_0_0 = blocks.multiply_const_ff(1/(agc_integration_const))
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(2000, 1/2000, 4000, 1)
        self.blocks_integrate_xx_0_0 = blocks.integrate_ff(int(agc_integration_const), 1)
        self.blocks_integrate_xx_0 = blocks.integrate_ff(int(agc_integration_const), 1)
        self.blocks_float_to_uchar_0 = blocks.float_to_uchar()
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, '/home/tbbg/rx_data_raw', False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/home/tbbg/rx_data', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_add_const_vxx_0_0_0 = blocks.add_const_ff(0)
        self.blocks_add_const_vxx_0_0 = blocks.add_const_ff(center_frequency_offset_error)
        self._bb_gain_display_tool_bar = Qt.QToolBar(self)

        if None:
            self._bb_gain_display_formatter = None
        else:
            self._bb_gain_display_formatter = lambda x: str(x)

        self._bb_gain_display_tool_bar.addWidget(Qt.QLabel('bb_gain_display' + ": "))
        self._bb_gain_display_label = Qt.QLabel(str(self._bb_gain_display_formatter(self.bb_gain_display)))
        self._bb_gain_display_tool_bar.addWidget(self._bb_gain_display_label)
        self.top_grid_layout.addWidget(self._bb_gain_display_tool_bar)
        self._baud_rate_display_tool_bar = Qt.QToolBar(self)

        if None:
            self._baud_rate_display_formatter = None
        else:
            self._baud_rate_display_formatter = lambda x: eng_notation.num_to_str(x)

        self._baud_rate_display_tool_bar.addWidget(Qt.QLabel('baud_rate_display' + ": "))
        self._baud_rate_display_label = Qt.QLabel(str(self._baud_rate_display_formatter(self.baud_rate_display)))
        self._baud_rate_display_tool_bar.addWidget(self._baud_rate_display_label)
        self.top_grid_layout.addWidget(self._baud_rate_display_tool_bar)
        self.analog_fm_demod_cf_0 = analog.fm_demod_cf(
        	channel_rate=samp_rate,
        	audio_decim=1,
        	deviation=(delta_f),
        	audio_pass=delta_f * 3,
        	audio_stop=delta_f * 7,
        	gain=1.0,
        	tau=0,
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fm_demod_cf_0, 0), (self.root_raised_cosine_filter_0, 0))
        self.connect((self.blocks_add_const_vxx_0_0, 0), (self.blocks_float_to_uchar_0, 0))
        self.connect((self.blocks_add_const_vxx_0_0, 0), (self.blocks_repeat_0_0, 0))
        self.connect((self.blocks_add_const_vxx_0_0_0, 0), (self.epy_block_0, 1))
        self.connect((self.blocks_complex_to_float_0, 1), (self.qtgui_time_sink_x_0_0, 2))
        self.connect((self.blocks_complex_to_float_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_float_to_uchar_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_float_to_uchar_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.blocks_multiply_const_vxx_1_0_0, 0))
        self.connect((self.blocks_integrate_xx_0_0, 0), (self.blocks_multiply_const_vxx_1_0_0_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_1_0_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0_0_0, 0), (self.blocks_add_const_vxx_0_0_0, 0))
        self.connect((self.blocks_repeat_0_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_repeat_0_0_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_repeat_0_0_1, 0), (self.qtgui_time_sink_x_0, 2))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_add_const_vxx_0_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.blocks_repeat_0_0_1, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.blocks_repeat_0_0_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_fm_demod_cf_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.blocks_integrate_xx_0_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.qtgui_time_sink_x_0_0, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "UHF_RX")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_center_frequency_offset_error(self):
        return self.center_frequency_offset_error

    def set_center_frequency_offset_error(self, center_frequency_offset_error):
        self.center_frequency_offset_error = center_frequency_offset_error
        self.blocks_add_const_vxx_0_0.set_k(self.center_frequency_offset_error)

    def get_bps(self):
        return self.bps

    def set_bps(self, bps):
        self.bps = bps
        self.set_baud_rate(self.bps * 2 / self.M)
        self.set_baud_rate_0(self.bps * 2 / self.M)
        self.set_delta_f(1.1 * self.bps)
        self.set_samp_per_bit((int)(self.samp_rate * (1 / self.bps)))

    def get_M(self):
        return self.M

    def set_M(self, M):
        self.M = M
        self.set_bandwidth(self.M * self.delta_f)
        self.set_baud_rate(self.bps * 2 / self.M)
        self.set_baud_rate_0(self.bps * 2 / self.M)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samp_per_bit((int)(self.samp_rate * (1 / self.bps)))
        self.set_samp_per_symbol(self.samp_rate * (1 / self.baud_rate))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 10e3, 3e3, firdes.WIN_HAMMING, 6.76))
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(10 * self.samp_rate / self.baud_rate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate )
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.baud_rate, 0.35, (int) (1e3)))

    def get_baud_rate(self):
        return self.baud_rate

    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate
        self.set_baud_rate_display(self._baud_rate_display_formatter(self.baud_rate))
        self.set_samp_per_symbol(self.samp_rate * (1 / self.baud_rate))
        self.qtgui_time_sink_x_0.set_samp_rate(10 * self.samp_rate / self.baud_rate)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, self.baud_rate, 0.35, (int) (1e3)))

    def get_samp_per_symbol(self):
        return self.samp_per_symbol

    def set_samp_per_symbol(self, samp_per_symbol):
        self.samp_per_symbol = samp_per_symbol
        self.set_samp_per_symbol_display(self._samp_per_symbol_display_formatter(self.samp_per_symbol))

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.set_rf_gain_display(self._rf_gain_display_formatter(self.rf_gain))
        self.osmosdr_source_0.set_gain(self.rf_gain, 0)

    def get_packet_bits(self):
        return self.packet_bits

    def set_packet_bits(self, packet_bits):
        self.packet_bits = packet_bits
        self.set_payload_bits(self.packet_bits - self.header_bits)

    def get_if_gain(self):
        return self.if_gain

    def set_if_gain(self, if_gain):
        self.if_gain = if_gain
        self.set_if_gain_display(self._if_gain_display_formatter(self.if_gain))
        self.osmosdr_source_0.set_if_gain(self.if_gain, 0)

    def get_header_bits(self):
        return self.header_bits

    def set_header_bits(self, header_bits):
        self.header_bits = header_bits
        self.set_payload_bits(self.packet_bits - self.header_bits)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_freq_display(self._freq_display_formatter(self.freq))
        self.osmosdr_source_0.set_center_freq(self.freq, 0)

    def get_delta_f(self):
        return self.delta_f

    def set_delta_f(self, delta_f):
        self.delta_f = delta_f
        self.set_bandwidth(self.M * self.delta_f)
        self.epy_block_0.symbol_delta_f = self.delta_f

    def get_bb_gain(self):
        return self.bb_gain

    def set_bb_gain(self, bb_gain):
        self.bb_gain = bb_gain
        self.set_bb_gain_display(self._bb_gain_display_formatter(self.bb_gain))
        self.osmosdr_source_0.set_bb_gain(self.bb_gain, 0)

    def get_samp_per_symbol_display(self):
        return self.samp_per_symbol_display

    def set_samp_per_symbol_display(self, samp_per_symbol_display):
        self.samp_per_symbol_display = samp_per_symbol_display
        Qt.QMetaObject.invokeMethod(self._samp_per_symbol_display_label, "setText", Qt.Q_ARG("QString", self.samp_per_symbol_display))

    def get_samp_per_bit(self):
        return self.samp_per_bit

    def set_samp_per_bit(self, samp_per_bit):
        self.samp_per_bit = samp_per_bit

    def get_rf_gain_display(self):
        return self.rf_gain_display

    def set_rf_gain_display(self, rf_gain_display):
        self.rf_gain_display = rf_gain_display
        Qt.QMetaObject.invokeMethod(self._rf_gain_display_label, "setText", Qt.Q_ARG("QString", self.rf_gain_display))

    def get_payload_bits(self):
        return self.payload_bits

    def set_payload_bits(self, payload_bits):
        self.payload_bits = payload_bits

    def get_if_gain_display(self):
        return self.if_gain_display

    def set_if_gain_display(self, if_gain_display):
        self.if_gain_display = if_gain_display
        Qt.QMetaObject.invokeMethod(self._if_gain_display_label, "setText", Qt.Q_ARG("QString", self.if_gain_display))

    def get_freq_display(self):
        return self.freq_display

    def set_freq_display(self, freq_display):
        self.freq_display = freq_display
        Qt.QMetaObject.invokeMethod(self._freq_display_label, "setText", Qt.Q_ARG("QString", self.freq_display))

    def get_freq_0(self):
        return self.freq_0

    def set_freq_0(self, freq_0):
        self.freq_0 = freq_0

    def get_demod_offset(self):
        return self.demod_offset

    def set_demod_offset(self, demod_offset):
        self.demod_offset = demod_offset
        self.epy_block_0.demod_offset = self.demod_offset
        self.osmosdr_source_0.set_bandwidth(self.bandwidth * 10 + self.demod_offset * 2, 0)

    def get_bb_gain_display(self):
        return self.bb_gain_display

    def set_bb_gain_display(self, bb_gain_display):
        self.bb_gain_display = bb_gain_display
        Qt.QMetaObject.invokeMethod(self._bb_gain_display_label, "setText", Qt.Q_ARG("QString", self.bb_gain_display))

    def get_baud_rate_display(self):
        return self.baud_rate_display

    def set_baud_rate_display(self, baud_rate_display):
        self.baud_rate_display = baud_rate_display
        Qt.QMetaObject.invokeMethod(self._baud_rate_display_label, "setText", Qt.Q_ARG("QString", self.baud_rate_display))

    def get_baud_rate_0(self):
        return self.baud_rate_0

    def set_baud_rate_0(self, baud_rate_0):
        self.baud_rate_0 = baud_rate_0

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.osmosdr_source_0.set_bandwidth(self.bandwidth * 10 + self.demod_offset * 2, 0)

    def get_agc_integration_const(self):
        return self.agc_integration_const

    def set_agc_integration_const(self, agc_integration_const):
        self.agc_integration_const = agc_integration_const
        self.blocks_multiply_const_vxx_1_0_0.set_k(1/(self.agc_integration_const))
        self.blocks_multiply_const_vxx_1_0_0_0.set_k(1/(self.agc_integration_const))




def argument_parser():
    parser = ArgumentParser()
    return parser


def main(top_block_cls=UHF_RX, options=None):
    if options is None:
        options = argument_parser().parse_args()

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
