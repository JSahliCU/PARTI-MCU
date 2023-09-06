    
def ber_estimator(verbose=False, max_errors_per_clip_range=5):
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

    total_number_of_clips = int(len(transmitted_bits)/clip_range)

    for i in range(0, total_number_of_clips):
        clipped_transmitted_bits = transmitted_bits[i*clip_range:(i+1)*(clip_range)]
        min_number_of_errors_per_i = clip_range
        # Search for the minimum number of errors caused by the start of the data sequence
        for tau in range(len(received_bits) - len(clipped_transmitted_bits)):
            error_bits = np.abs(np.ndarray.astype(clipped_transmitted_bits, np.byte) \
                - np.ndarray.astype(received_bits[tau:tau+len(clipped_transmitted_bits)], np.byte))
            temp = np.sum(error_bits)
            if temp < min_number_of_errors_per_i:
                min_number_of_errors_per_i = temp

            if temp < number_of_errors:
                number_of_errors = temp
                tau_min = tau

            if temp < max_errors_per_clip_range:
                number_of_errors = temp
                tau_min = tau
                break
        print('{0}/{1}'.format(min_number_of_errors_per_i,clip_range) \
              + ' errors found in clip index i=' + str(i) \
              + '/' + str(total_number_of_clips), end='\r')
        
        if number_of_errors < max_errors_per_clip_range:
            ith_kbit = i
            break

    # Once the first fully correct clip range is found, 
    # look for the last block that has less than max_errors_per_clip_range
    end_number_of_errors = clip_range
    end_tau = tau_min
    total_errors = 0
    for tau in range(tau_min, len(received_bits) - len(clipped_transmitted_bits), clip_range):
        clipped_transmitted_bits = transmitted_bits[i*clip_range:(i+1)*(clip_range)]
        error_bits = np.abs(np.ndarray.astype(clipped_transmitted_bits, np.byte) \
            - np.ndarray.astype(received_bits[tau:tau+len(clipped_transmitted_bits)], np.byte))
        temp = np.sum(error_bits)

        end_number_of_errors = temp
        end_tau = tau + clip_range

        if temp > max_errors_per_clip_range:
            break
        else:
            total_errors += temp

        i += 1

    # min_error_bits = np.abs(np.ndarray.astype(transmitted_bits, np.byte) \
    #         - np.ndarray.astype(received_bits[tau_min:tau_min+len(transmitted_bits)], np.byte))

    bit_error_rate = total_errors / (end_tau - tau_min)

    if verbose:
        print()
        print('TX Data Length: ' + str(len(transmitted_bits)))
        print('RX Data Length: ' + str(len(received_bits)))
        print('Clean data found from {0} to {1}, for a total length {2}'.format(tau_min, end_tau, (end_tau - tau_min)))
        print('Errors in the first clip range {0}'.format(number_of_errors))
        print('Errors in the last clip range {0}'.format(end_number_of_errors))
        print('Bit Error Rate (BER): ' + str(bit_error_rate))
        print()
        print(str(received_bits[tau_min:tau_min+40]))
        print(str(transmitted_bits[ith_kbit*clip_range:ith_kbit*clip_range+40]))

    return bit_error_rate, number_of_errors, len(transmitted_bits), len(received_bits), tau_min

if __name__ == '__main__':
    ber_estimator(verbose=True)