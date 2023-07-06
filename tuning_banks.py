import RPi.GPIO as GPIO
import led_mappings

def tune_hf():
    # TODO implement the actual hf tuning code
    # Don't forget to update the heartbeat file
    GPIO.output(led_mappings.led_to_bcm_mapping.HF_L1_SOLID, GPIO.HIGH)
    GPIO.output(led_mappings.led_to_bcm_mapping.HF_L2_SOLID, GPIO.HIGH)