import cv2
import RPi.GPIO as GPIO
import threading
import time
from ultralytics import YOLO
from gtts import gTTS
from io import BytesIO
import pygame
from googletrans import Translator
import serial
from pushbullet import pushbullet as pbclient


# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Setup GPIO pins
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Button
GPIO.setup(2, GPIO.OUT)  # Ultrasonic sensor 1 TRIG
GPIO.setup(3, GPIO.IN)   # Ultrasonic sensor 1 ECHO
GPIO.setup(17, GPIO.OUT)   # Ultrasonic sensor 2 TRIG
GPIO.setup(27, GPIO.IN)    # Ultrasonic sensor 2 ECHO
GPIO.setup(10, GPIO.OUT)  # Ultrasonic sensor 3 TRIG
GPIO.setup(9, GPIO.IN)   # Ultrasonic sensor 3 ECHO
GPIO.setup(5, GPIO.OUT)  # Vibration Motor 1
#GPIO.setup(20, GPIO.OUT)  # Vibration Motor 2
#GPIO.setup(21, GPIO.OUT)  # Vibration Motor 3

# Initialize ultrasonic sensors and motors
GPIO.output(2, False)
GPIO.output(17, False)
GPIO.output(10, False)
GPIO.output(5, False)

# Initialize Pygame for audio
pygame.init()
pygame.mixer.init()

# Create a lock for shared resources
lock = threading.Lock()

# Function to handle ultrasonic sensor monitoring
def ultrasonic_monitoring():
    while True:
        with lock:
            distance1 = ultrasonic(2, 3)  # Ultrasonic sensor 1
            distance2 = ultrasonic(17, 27)    # Ultrasonic sensor 2
            distance3 = ultrasonic(10, 9)  # Ultrasonic sensor 3

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
            if min_distance <10:
                GPIO.output(5, True)  # Vibration Motor 1
                print("Minimum Distance2:", min_distance)
                time.sleep(4)
                GPIO.output(5, False)
           # if min_distance < 10 and min_sensor == "Ultrasonic 1":
            #    GPIO.output(5, True)  # Vibration Motor 1
             #   print("Minimum Distance2:", min_distance)
              #  time.sleep(4)
               # GPIO.output(5, False)
            #elif min_distance < 10 and min_sensor == "Ultrasonic 2":
             #   GPIO.output(5, True)  # Vibration Motor 2
              #  print("Minimum Distance2:", min_distance)
               # time.sleep(4)
                #GPIO.output(5, False)
            #elif min_distance < 10 and min_sensor == "Ultrasonic 3":
             #   GPIO.output(5, True)  # Vibration Motor 3
              #  print("Minimum Distance2:", min_distance)
               # time.sleep(4)
                #GPIO.output(5, False)
            time.sleep(0.1)

# Function to handle button press and image capture
def button_handler():
    print('Waiting for button press...')
    while True:
        if GPIO.input(22) == GPIO.HIGH:
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

#function for localization and communication
def read_gps_data():
   
    pb = pbclient.Pushbullet("o.OvzdycciHIRvvwJKmEJXEwj5Si3gTEuJ")
    mydev = pb.get_device('Samsung SM-A736B')
                    
    ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)  # Adjust port and baud rate as needed

    try:
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line.startswith('$GPGGA'):
                data = line.split(',')
                if len(data) >= 10 and data[6] != '' and data[7] != '':
                    latitude = float(data[2][:2]) + float(data[2][2:]) / 60
                    if data[3] == 'S':
                        latitude = -latitude
                    longitude = float(data[4][:3]) + float(data[4][3:]) / 60
                    if data[5] == 'W':
                        longitude = -longitude
                    map_link = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"    
                    push = mydev.push_note("message",str(map_link))
                    print('notification sent to user')
                    print(f'current location is{map_link}')

                    return latitude, longitude, map_link
    except KeyboardInterrupt:
        print("Exiting GPS reader")
    finally:
        ser.close()


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
            class_name = names[int(c)]
            print(class_name)

            # Translate the class name to Arabic
            #translation = translator.translate(class_name, dest='ar')
            #translated_text = translation.text
            #print(translated_text)

            # Convert translated text to audio and play
            mp3_fp = BytesIO()
            tts = gTTS(class_name, lang='ar')
            tts.save('translated_audio.mp3')
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
        
            # Play the translated audio
            sound = pygame.mixer.Sound(mp3_fp)
            playing = sound.play()
            while playing.get_busy():
                 pygame.time.delay(100)
            time.sleep(0.5)
            mp3_fp.close()

def run_read_gps_data():
    read_gps_data()
    threading.Timer(15, run_read_gps_data).start()

# Start ultrasonic monitoring thread
ultrasonic_thread = threading.Thread(target=ultrasonic_monitoring)
ultrasonic_thread.daemon = True  # Set as daemon thread to exit when main thread exits
ultrasonic_thread.start()

localization_thread = threading.Thread(target = read_gps_data)
localization_thread.daemon = True
localization_thread.start()



#run_read_gps_data()

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
