"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import time
import datetime

class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

    gain_table = (
         #rf,   if,     bb
         (0,     0,     0),
         (0,     0,     2),
         (0,     0,     4),
         (0,     0,     6),
         (0,     8,     0),
         (0,     8,     2),
         (0,     8,     4),
         (0,     8,     6),
         (0,     8,     8),
         (0,     8,     10),
         (0,     8,     12),
         (0,     8,     14),
         (0,     16,    8),
         (0,     16,    10),
         (0,     16,    12),
         (0,     16,    14),
         (0,     16,    16),
         (0,     16,    18),
         (0,     16,    20),
         (0,     16,    22),
         (0,     24,    16),
         (0,     24,    18),
         (0,     24,    20),
         (0,     24,    22),
         (0,     24,    24),
         (0,     24,    26),
         (0,     24,    28),
         (0,     24,    30),
         (11,    24,    20),
         (11,    24,    22),
         (11,    24,    24),
         (11,    24,    26),
         (11,    24,    28),
         (11,    24,    30),
         (11,    32,    24),
         (11,    32,    26),
         (11,    32,    28),
         (11,    32,    30),
         (11,    32,    32),
         (11,    32,    34),
         (11,    32,    36),
         (11,    32,    38),
         (11,    40,    32),
         (11,    40,    34),
         (11,    40,    36),
         (11,    40,    38),
         (11,    40,    40),
         (11,    40,    42),
         (11,    40,    44),
         (11,    40,    46),
         (11,    40,    48),
         (11,    40,    50),
         (11,    40,    52),
         (11,    40,    54),
         (11,    40,    56),
         (11,    40,    58),
         (11,    40,    60),
         (11,    40,    62),
    )

    log_file = 'gain_log.csv'

    def __init__(self, 
                 goal_input_level=1.0, hysteresis=1.5, update_period=0.5, auto_log_time_min=15,
                 callback_rf_gain=None, callback_if_gain=None, callback_bb_gain=None):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.goal_input_level = goal_input_level
        self.hysteresis = hysteresis
        self.update_period = update_period
        self.callback_rf_gain = callback_rf_gain
        self.callback_if_gain = callback_if_gain
        self.callback_bb_gain = callback_bb_gain

        self.gain_table_index = 8
        self.log_index = 0
        self.auto_log_time_min = auto_log_time_min
        self.log_index_limit = 60 * auto_log_time_min / update_period

        import os
        cwd = os.getcwd()
        print(cwd)

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        
        def log():
            with open(blk.log_file, mode='+a') as f:
                gain_table_tuple = blk.gain_table[self.gain_table_index]
                rf_gain = gain_table_tuple[0]
                if_gain = gain_table_tuple[1]
                bb_gain = gain_table_tuple[2]
                log_msg = ','.join(
                    map(str, 
                        [input_items[-1][-1], rf_gain, if_gain, bb_gain]
                    )
                )
                print(str(datetime.datetime.now()) + "UTC " + log_msg, file=f)

        if input_items[-1][-1] > (self.goal_input_level + self.hysteresis/2):
            log()
            self.decrease_gain()

        if input_items[-1][-1] < (self.goal_input_level - self.hysteresis/2):
            log()
            self.increase_gain() 
        
        if self.log_index >= self.log_index_limit:
            log()
        else:
            self.log_index += 1
        #output_items[0][:] = input_items[0] * self.example_param
        
        time.sleep(self.update_period)
        return 0 #len(output_items[0])

    def check_gain_table_index_limits(self):
        if self.gain_table_index < 0:
            self.gain_table_index = 0
        
        if self.gain_table_index >= len(blk.gain_table):
            self.gain_table_index = len(blk.gain_table) - 1

    def set_gain_from_gain_table(self):
        gain_table_tuple = blk.gain_table[self.gain_table_index]
        rf_gain = gain_table_tuple[0]
        if_gain = gain_table_tuple[1]
        bb_gain = gain_table_tuple[2]

        self.callback_rf_gain(rf_gain)
        self.callback_if_gain(if_gain)
        self.callback_bb_gain(bb_gain)

    def decrease_gain(self):
        self.gain_table_index -= 1
        self.check_gain_table_index_limits()
        self.set_gain_from_gain_table()

    def increase_gain(self):
        self.gain_table_index += 1
        self.check_gain_table_index_limits()
        self.set_gain_from_gain_table()
