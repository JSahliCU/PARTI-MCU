home_directory = '/home/tbbg/'

serial_number_file_location = home_directory + 'serial_number'

split_tune_file_location = home_directory + 'split_tune.txt'
solid_tune_file_location = home_directory + 'solid_tune.txt'
boot_mode_file_location = home_directory + 'boot.txt'

with open(serial_number_file_location, 'r') as f:
    sn = int(f.read())

if sn == 1:
    split_tune  = 33
    solid_tune  = 56
    boot_mode   = 'RX'
elif sn == 2:
    split_tune  = 65
    solid_tune  = 59
    boot_mode   = 'TX'
elif sn == 3:
    split_tune  = 59
    solid_tune  = 53
    boot_mode   = 'RX'
elif sn == 4:
    split_tune  = 60
    solid_tune  = 45
    boot_mode   = 'TX'
else:
    raise ValueError('Serial number {0} does not have a configuration'.format(sn))

with open(split_tune_file_location, 'w') as f:
    f.write(str(split_tune))

with open(solid_tune_file_location, 'w') as f:
    f.write(str(solid_tune))

with open(boot_mode_file_location, 'w') as f:
    f.write(boot_mode)

