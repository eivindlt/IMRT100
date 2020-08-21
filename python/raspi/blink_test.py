import time
import RPi.GPIO as GPIO

LED_PIN = 15

# BCM pin naming
GPIO.setmode(GPIO.BCM)

# Turn off GPIO warnings
GPIO.setwarnings(False)

# Set LED pin to output
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    
    # Loop until user terminates program
    while True:
            # Turn LED on
            GPIO.output(LED_PIN, GPIO.HIGH)
            for i in range (10):
                time_sleep = 0.1 * i
                #print LED on
                print("LED on")
                time.sleep(time_sleep)
                GPIO.output(LED_PIN, GPIO.LOW)
                print("LED off")
                time.sleep(time_sleep)

except KeyboardInterrupt:
    print("Terminated by user")

finally:
    # Cleanup
    GPIO.cleanup()
    print("Goodbye")
