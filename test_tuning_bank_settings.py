import tuning_banks

tb_split = tuning_banks.tuning_bank_split()
tb_solid = tuning_banks.tuning_bank_solid()

bank_select = input('Bank control selection, 1 for split, 2 for solid: ')

tb = tb_split
if int(bank_select) == 2:
    tb = tb_solid
    print('Solid bank selected')
else:
    print('Split bank selected')

while True:
    user_input = input('Enter capacitance setting for bank: ')
    if user_input == 'q' or user_input == 'quit()':
        break
    elif user_input == 'r' or user_input == 'reset()':
        tb.reset_capacitance()
    else:
        #print('Setting capacitance to ' + str(int(user_input)))
        tb.set_capacitance(int(user_input), debug=True)