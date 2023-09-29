#!/bin/bash

sudo apt-get install uhubctl

cp ./* ../
python configure.py
crontab < ./tbbg