# Pretty prints all of running data into a command prompt windows

with open('heartbeat.txt', 'r') as f:
    print(f.read())

with open('RX_TX.txt', 'r') as f:
    with open('band.txt', 'r') as f1:
        print('Mode: ' + f.read() + ' ' + f1.read())

with open('solid_tune.txt', 'r') as f:
    print('Solid Tune: ' + f.read() + ' pF')

with open('split_tune.txt', 'r') as f:
    print('Split Tune: ' + f.read() + ' pF')

print()
print('-----------------------------------------') 
print('Settings')

# https://www.raspberrypi-spy.co.uk/2012/09/getting-your-raspberry-pi-serial-number-using-python/
def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"
 
  return cpuserial

print('CPU Serial: ' + getserial())

with open('transceiver_state_interval.txt', 'r') as f:
    print('Transceiver State Interval: ' + f.read() + ' minutes')

with open('boot.txt', 'r') as f:
    print('Boot Mode: ' + f.read())