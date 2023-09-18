These programs were designed for the PARTI pucks project. This git repository is to be cloned on to the RPI within each PARTI puck. Then the following commands are to be run within the repo

1. pip install -r requirements.txt
1. run the install.sh file from the root directory of the project
1. Create a split_tune.txt and solid_tune.txt file in the ~/ (on the RPi) and populate them with the initial tuning capacitance values based on 'Tuning_Bank_Settings_\[yyyymmdd\].ods'. i.e (split_tune.txt contains only the string '43')
1. Create a boot.txt file that contains the desired boot mode of the device, i.e. the strings 'RX' or 'TX' only
1. Use quicklook.sh to monitor the last 20 minutes of samples
