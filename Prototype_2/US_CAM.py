import threading

import Object_Detection_2 as detection

import Ultrasonics_3 as US

import Jetson.GPIO as GPIO

import time



# Function to run object detection every 30 seconds

def detect_objects_periodically():

    while True:

        print("Running object detection...")

        detection.Detect_Objects()

        time.sleep(30)  # Wait for 30 seconds before the next detection



# Thread for obstacle avoidance to run continuously

def run_obstacle_avoidance():

    while True:

        US.Obstacle_Avoidance()

        time.sleep(0.1)



# Start threads

if __name__ == "__main__":

    try:

        obstacle_thread = threading.Thread(target=run_obstacle_avoidance)

        detect_thread = threading.Thread(target=detect_objects_periodically)



        # Start both threads

        obstacle_thread.start()

        detect_thread.start()



        # Keep both threads running

        obstacle_thread.join()

        detect_thread.join()



    except KeyboardInterrupt:

        print("Program interrupted by user. Cleaning up GPIO...")

        GPIO.cleanup()  # Clean up GPIO after program ends


