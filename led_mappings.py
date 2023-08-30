import enum

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

led_index_to_bcm_mapping ={
     1: 6,
     2: 13,
     3: 22,
     4: 5,
     5: 17,
     6: 27,
     7: 19
     }

led_to_bcm_mapping = enum(
    HF_L1_SOLID = led_index_to_bcm_mapping[1],
    HF_L2_SPLIT = led_index_to_bcm_mapping[2],
    HF_TX = led_index_to_bcm_mapping[3],
    HF_RX = led_index_to_bcm_mapping[4],
    UHF_TX = led_index_to_bcm_mapping[5],
    UHF_RX = led_index_to_bcm_mapping[6],
    MCU_ON = led_index_to_bcm_mapping[7],
    #MAIN_DISCO = led_index_to_bcm_mapping[8], # Main disconnect has no led on the interface v1a1a
)