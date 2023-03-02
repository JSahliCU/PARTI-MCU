from ADCPi import ADCPi
import datetime

adc = ADCPi(0x68, 0x68, 18)

log_file = 'mcp3422.csv'

# set one shot conversion mode
adc.set_conversion_mode(0) 

channel_1 = adc.read_voltage(1)*(3.3 / 5)
channel_2 = adc.read_voltage(2)*(3.3 / 5) - (2.75 - 1.675)

with open(log_file, 'a') as f:
    print(str(datetime.datetime.now()) + "UTC," + str(channel_1) + ", " + str(channel_2), file=f)

# from MCP342x import MCP342x
# 
# adc = MCP342x(1, int(0x68), device='MCP3422', channel=0, gain=1, resolution=18,
#               continuous_mode=False, scale_factor=1.0, offset=0.0)
# 
# print(adc.convert_and_read())