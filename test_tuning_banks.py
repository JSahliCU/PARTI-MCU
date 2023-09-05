import tuning_banks

tb_split = tuning_banks.tuning_bank_split()
tb_solid = tuning_banks.tuning_bank_solid()

for tb, tb_name in [(tb_split, 'split'), (tb_solid, 'solid')]:
    for i, relay in enumerate(tb.relays):
        tb.port_states[relay.set_pin] = False
        tb.sync_port_states()
        tb.port_states[relay.set_pin] = True
        input(tb_name + ' set ' + str(i) + '    ' + str(relay.cap_value) + 'pF')

        tb.port_states[relay.reset_pin] = False
        tb.sync_port_states()
        tb.port_states[relay.reset_pin] = True
        input(tb_name + 'reset ' + str(i) + '    ' + str(relay.cap_value) + 'pF')