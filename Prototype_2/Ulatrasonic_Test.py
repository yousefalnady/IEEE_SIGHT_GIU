import Jetson.GPIO as GPIO

import time



# Set GPIO pin numbers

TRIG = 21  # Pin 40

ECHO = 20  # Pin 38



# Setup GPIO mode and pins

GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIG, GPIO.OUT)

GPIO.setup(ECHO, GPIO.IN)



def measure_distance():

    # Ensure trigger is low

    GPIO.output(TRIG, False)

    time.sleep(0.5)

    

    # Send 10us pulse to trigger

    GPIO.output(TRIG, True)

    time.sleep(0.00001)

    GPIO.output(TRIG, False)

    

    # Measure time between sending and receiving the signal

    while GPIO.input(ECHO) == 0:

        pulse_start = time.time()

    

    while GPIO.input(ECHO) == 1:

        pulse_end = time.time()

    

    # Calculate pulse duration and convert to distance (cm)

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    return round(distance, 2)



try:

    while True:

        distance = measure_distance()

        print(f"Distance: {distance} cm")

        time.sleep(5)



except KeyboardInterrupt:

    print("Measurement stopped by user")

    GPIO.cleanup()


