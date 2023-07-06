from ADCPi import ADCPi
import datetime
import math

adc = ADCPi(0x68, 0x68, 18)

log_file = 'mcp3422.csv'

# set one shot conversion mode
adc.set_conversion_mode(0) 

channel_1 = adc.read_voltage(1)*(3.3 / 5) + (3.3 / 2)
channel_2 = adc.read_voltage(2)*(3.3 / 5)

# Convert to face temperature
# Conversion values based on Vishay NTCLE428E3103F524A, Table 3 of datasheet
R_25 = 10e3
R_25_tol = 0.01
B_25_over_85 = 3435
B_25_over_85_5ol = 0.01

R_T = channel_1 * 10e3 / (3.3 - channel_1)

temp = math.log(R_T / R_25) / B_25_over_85
temp += 1.0 / (25 + 273.15)
puck_face_temperature = (1.0 / temp) - 273.15

with open(log_file, 'a') as f:
    print(str(datetime.datetime.now()) + "UTC," + str(channel_1) + ", " + str(channel_2) + ", " + str(puck_face_temperature), file=f)

# from MCP342x import MCP342x
# 
# adc = MCP342x(1, int(0x68), device='MCP3422', channel=0, gain=1, resolution=18,
#               continuous_mode=False, scale_factor=1.0, offset=0.0)
# 
# print(adc.convert_and_read())