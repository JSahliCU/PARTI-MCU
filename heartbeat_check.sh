#!/bin/bash

# Export the python path variable so that gnuradio functions correctly
export PYTHONPATH=/usr/local/lib/python3/dist-packages

# Export the display variable so that all remotely launched programs
#    show up on the correct display
export DISPLAY=:0

# Store the pid
ps cax | grep -f 'run_pid.txt'
if [ $? -eq 0 ]; then
    echo 'Running'
    python heartbeat_check.py
    if [ $? -eq 0 ]; then
        echo 'Heartbeat looks good'
    else
        kill -9 $(cat 'run_pid.txt')
        echo $(date -u) 'Attempting reboot because heartbeat out of date' >> error.log
        python run.py & disown
    fi
else
    echo $(date -u) 'Attempting reboot because PID not detected' >> error.log
    python run.py & disown
fi