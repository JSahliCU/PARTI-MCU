#!/bin/bash
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