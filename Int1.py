import cv2
import RPi.GPIO as GPIO
import threading
import time
from ultralytics import YOLO
from gtts import gTTS
from io import BytesIO
import pygame
from googletrans import Translator

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Setup GPIO pins
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Button
GPIO.setup(13, GPIO.OUT)  # Ultrasonic sensor 1 TRIG
GPIO.setup(11, GPIO.IN)   # Ultrasonic sensor 1 ECHO
GPIO.setup(2, GPIO.OUT)   # Ultrasonic sensor 2 TRIG
GPIO.setup(3, GPIO.IN)    # Ultrasonic sensor 2 ECHO
GPIO.setup(17, GPIO.OUT)  # Ultrasonic sensor 3 TRIG
GPIO.setup(27, GPIO.IN)   # Ultrasonic sensor 3 ECHO
GPIO.setup(18, GPIO.OUT)  # Vibration Motor 1
GPIO.setup(20, GPIO.OUT)  # Vibration Motor 2
GPIO.setup(21, GPIO.OUT)  # Vibration Motor 3

# Initialize ultrasonic sensors and motors
GPIO.output(13, False)
GPIO.output(2, False)
GPIO.output(17, False)
GPIO.output(18, False)
GPIO.output(20, False)
GPIO.output(21, False)

# Initialize Pygame for audio
pygame.init()
pygame.mixer.init()

# Create a lock for shared resources
lock = threading.Lock()

# Function to handle ultrasonic sensor monitoring
def ultrasonic_monitoring():
    while True:
        with lock:
            distance1 = ultrasonic(11, 13)  # Ultrasonic sensor 1
            distance2 = ultrasonic(3, 2)    # Ultrasonic sensor 2
            distance3 = ultrasonic(27, 17)  # Ultrasonic sensor 3

            print("Distance 1:", distance1, "cm")
            print("Distance 2:", distance2, "cm")
            print("Distance 3:", distance3, "cm")

            min_distance = min(distance1, distance2, distance3)
            if min_distance == distance1:
                min_sensor = "Ultrasonic 1"
            elif min_distance == distance2:
                min_sensor = "Ultrasonic 2"
            else:
                min_sensor = "Ultrasonic 3"
            print("Minimum Distance:", min_distance)
            print(min_sensor)
            if min_distance < 10 and min_sensor == "Ultrasonic 1":
                GPIO.output(18, True)  # Vibration Motor 1
                print("Minimum Distance2:", min_distance)
                time.sleep(4)
                GPIO.output(18, False)
            elif min_distance < 10 and min_sensor == "Ultrasonic 2":
                GPIO.output(20, True)  # Vibration Motor 2
                print("Minimum Distance2:", min_distance)
                time.sleep(4)
                GPIO.output(20, False)
            elif min_distance < 10 and min_sensor == "Ultrasonic 3":
                GPIO.output(21, True)  # Vibration Motor 3
                print("Minimum Distance2:", min_distance)
                time.sleep(4)
                GPIO.output(21, False)
            time.sleep(0.1)

# Function to handle button press and image capture
def button_handler():
    print('Waiting for button press...')
    while True:
        if GPIO.input(4) == GPIO.HIGH:
            print("Button pressed!")
            with lock:
                capture_image()
                process_image()
            time.sleep(1)  # Debounce delay

# Ultrasonic sensor function
def ultrasonic(GPIO_TRIG, GPIO_ECHO):
    GPIO.output(GPIO_TRIG, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIG, False)

    pulse_start = time.time()
    pulse_end = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

# Function to capture image
def capture_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    ret, frame = cap.read()

    if ret:
        cv2.imwrite('captured_image.jpg', frame)
        print("Image captured successfully.")
    else:
        print("Error: Could not capture image.")

    cap.release()

# Function to process image
def process_image():
    model = YOLO('yolov8n.pt')

    print('Processing image...')
    results = model("captured_image.jpg", conf=0.4, show=True)

    names = model.names

    for r in results:
        for c in r.boxes.cls:
            print(names[int(c)])
            ar = translator.translate(names[int(c)], dest='ar')
            print(ar)
            mp3_fp = BytesIO()
            tts = gTTS(ar, lang='ar')
            tts.save('hello.mp3')
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            sound = pygame.mixer.Sound(mp3_fp)
            playing = sound.play()
            while playing.get_busy():
                pygame.time.delay(100)
            time.sleep(0.5)
            mp3_fp.close()

# Start ultrasonic monitoring thread
ultrasonic_thread = threading.Thread(target=ultrasonic_monitoring)
ultrasonic_thread.daemon = True  # Set as daemon thread to exit when main thread exits
ultrasonic_thread.start()

# Start button handler thread
button_thread = threading.Thread(target=button_handler)
button_thread.daemon = True  # Set as daemon thread to exit when main thread exits
button_thread.start()

# Main thread waits indefinitely
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()