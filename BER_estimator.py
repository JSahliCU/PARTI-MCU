    
def ber_estimator(verbose=False):
    import numpy as np

    with open("tx_data", 'rb') as transmitted_binary:
        with open("rx_data", 'rb') as received_binary:
            transmitted_array = np.asarray(bytearray(transmitted_binary.read()))
            received_array = np.asarray(bytearray(received_binary.read()))

    transmitted_bits = np.unpackbits(transmitted_array)
    received_bits = np.unpackbits(received_array)
    number_of_errors = len(received_bits)
    tau_min = 0

    clip_range = 1000 # bits
    ith_kbit = -1
    for i in range(0, int(len(transmitted_bits)/clip_range)):
        clipped_transmitted_bits = transmitted_bits[i*clip_range:(i+1)*(clip_range)]
        
        # Search for the minimum number of errors caused by the start of the data sequence
        for tau in range(len(received_bits) - len(clipped_transmitted_bits)):
            error_bits = np.abs(np.ndarray.astype(clipped_transmitted_bits, np.byte) \
                - np.ndarray.astype(received_bits[tau:tau+len(clipped_transmitted_bits)], np.byte))
            temp = np.sum(error_bits)
            if temp < number_of_errors:
                number_of_errors = temp
                tau_min = tau

            if temp == 0:
                number_of_errors = temp
                tau_min = tau
                break
        print(i, number_of_errors, tau_min)
        if number_of_errors == 0:
            ith_kbit = i
            break

    # min_error_bits = np.abs(np.ndarray.astype(transmitted_bits, np.byte) \
    #         - np.ndarray.astype(received_bits[tau_min:tau_min+len(transmitted_bits)], np.byte))

    bit_error_rate = number_of_errors / (clip_range)

    if verbose:
        print('Errors: ' + str(number_of_errors))
        print('TX Data Length: ' + str(len(transmitted_bits)))
        print('RX Data Length: ' + str(len(received_bits)))
        print('Bit Error Rate (BER): ' + str(bit_error_rate))
        print('Tau: ' + str(tau_min))
        print(str(received_bits[tau_min:tau_min+40]))
        print(str(transmitted_bits[ith_kbit*1000:ith_kbit*1000+40]))

    return bit_error_rate, number_of_errors, len(transmitted_bits), len(received_bits), tau_min

if __name__ == '__main__':
    ber_estimator(verbose=True)