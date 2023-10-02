#!/bin/bash

python plotting_quicklook.py &

lxterminal -e watch python pretty_print_log.py &
lxterminal -e watch tail -10 error.log &