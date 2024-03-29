import threading
import time
import serial
import cv2
from pushbullet import pushbullet as pbclient
from ultralytics import YOLO
import RPi.GPIO as GPIO
from gtts import gTTS
import pygame
from io import BytesIO

# Global variables
stop_threads = False

# Pushbullet setup
pb = pbclient.Pushbullet("o.OvzdycciHIRvvwJKmEJXEwj5Si3gTEuJ")
mydev = pb.get_device('Samsung SM-A736B')

# GPIO setup
BUTTON_PIN = 4  # Change this to the GPIO pin connected to your button
GPIO_ECHO1 = 13
GPIO_TRIG1 = 11
GPIO_ECHO2 = 2
GPIO_TRIG2 = 3
GPIO_ECHO3 = 17
GPIO_TRIG3 = 27
Vibration_Motor1 = 18
Vibration_Motor2 = 20
Vibration_Motor3 = 21

GPIO.setup(GPIO_TRIG1, GPIO.OUT)
GPIO.setup(GPIO_ECHO1, GPIO.IN)
GPIO.setup(GPIO_TRIG2, GPIO.OUT)
GPIO.setup(GPIO_ECHO2, GPIO.IN)
GPIO.setup(GPIO_TRIG3, GPIO.OUT)
GPIO.setup(GPIO_ECHO3, GPIO.IN)
GPIO.setup(Vibration_Motor1, GPIO.OUT)
GPIO.setup(Vibration_Motor2, GPIO.OUT)
GPIO.setup(Vibration_Motor3, GPIO.OUT)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Function to read GPS data
def read_gps_data():
    ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)  # Adjust port and baud rate as needed

    try:
        while not stop_threads:
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
                    # Send notification to caregiver every 2 hours
                    if time.time() % (2*3600) < 1:
                        push = mydev.push_note("Location Update", map_link)
                    time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting GPS reader")
    finally:
        ser.close()

# Function to capture image and perform object detection
def capture_and_detect():
    model = YOLO('yolov8n.pt')
    pygame.init()
    pygame.mixer.init()
    
    while not stop_threads:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cap.release()

            if ret:
                cv2.imwrite('captured_image.jpg', frame)
                print("Image captured successfully.")
            else:
                print("Error: Could not capture image.")
                continue

            results = model("captured_image.jpg", conf=0.4, show=True)
            names = model.names

            for r in results:
                for c in r.boxes.cls:
                    object_name = names[int(c)]
                    print(object_name)
                    # Generate voice output for the detected object
                    tts = gTTS(object_name, lang='en')
                    mp3_fp = BytesIO()
                    tts.save(mp3_fp)
                    mp3_fp.seek(0)
                    pygame.mixer.music.load(mp3_fp)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)
                    mp3_fp.close()
                    time.sleep(0.5)

# Function to read ultrasonic sensors and trigger vibration motors
def ultrasonic_and_vibration():
    GPIO.setwarnings(False)


    GPIO.output(GPIO_TRIG1, False)
    GPIO.output(GPIO_TRIG2, False)
    GPIO.output(GPIO_TRIG3, False)
    GPIO.output(Vibration_Motor1, False)
    GPIO.output(Vibration_Motor2, False)
    GPIO.output(Vibration_Motor3, False)

    time.sleep(2)

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

    try:
        while not stop_threads:
            distance1 = ultrasonic(GPIO_TRIG1, GPIO_ECHO1)
            distance2 = ultrasonic(GPIO_TRIG2, GPIO_ECHO2)
            distance3 = ultrasonic(GPIO_TRIG3, GPIO_ECHO3)
            
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
            print("Minimum Distance:",min_distance)
            print(min_sensor)
            if min_distance < 10 and min_sensor=="Ultrasonic 1":
                GPIO.output(Vibration_Motor1, True)
                print("Minimum Distance2:",min_distance)
                time.sleep(4)
                GPIO.output(Vibration_Motor1, False)
            elif min_distance < 10 and min_sensor=="Ultrasonic 2":
                GPIO.output(Vibration_Motor2, True)
                print("Minimum Distance2:",min_distance)
                time.sleep(4)
           
                GPIO.output(Vibration_Motor2, False)
            elif min_distance < 10 and min_sensor=="Ultrasonic 3":
                GPIO.output(Vibration_Motor3, True)
                print("Minimum Distance2:",min_distance)
                time.sleep(4)	
            
                GPIO.output(Vibration_Motor3, False)            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == '__main__':
    try:
        # Create threads for GPS reading and ultrasonic sensing
        gps_thread = threading.Thread(target=read_gps_data)
        ultrasonic_thread = threading.Thread(target=ultrasonic_and_vibration)

        # Start the threads
        gps_thread.start()
        ultrasonic_thread.start()

        # Main loop to check button press and start object detection thread
        while True:
            if GPIO.input(BUTTON_PIN) == GPIO.LOW:
                # Button is pressed, start object detection thread
                camera_thread = threading.Thread(target=capture_and_detect)
                camera_thread.start()
                camera_thread.join()  # Wait for object detection to finish before checking the button again
            time.sleep(0.1)  # Add a small delay to prevent busy-waiting
    except KeyboardInterrupt:
        stop_threads = True
        gps_thread.join()
        ultrasonic_thread.join()
