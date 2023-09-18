from run import *

if __name__ == "__main__":
    try:
        # Run the main loop with the amplifier supplies off
        main(enable_amplifier_supplies=False)
    except Exception as inst:
        # Displays any exceptions, logs them into error log and blink front panel lights
        throw_error(inst.__str__())