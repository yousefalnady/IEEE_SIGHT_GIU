import cv2
from ultralytics import YOLO        #importing the ML library
from gtts import gTTS               #Google-Text-To-Speech API
from io import BytesIO              #File handling library to play audio
import pygame                       #for playing audio
from googletrans import Translator
import time
import RPi.GPIO as GPIO


GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering

GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

def capture_image():
    # Open a connection to the webcam (camera index 0 by default)
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Capture a single frame
    ret, frame = cap.read()

    # Save the captured frame to an image file
    if ret:
        cv2.imwrite('captured_image.jpg', frame)
        print("Image captured successfully.")
    else:
        print("Error: Could not capture image.")

    # Release the webcam
    cap.release()


print('waiting for button')
while True: # Run forever
    if GPIO.input(4) == GPIO.HIGH:
        print("Button was pushed!")
        break
print('pressed')

capture_image()

model = YOLO('yolov8n.pt')          #selecting the prediction model
pygame.init()
pygame.mixer.init()
translator = Translator(service_urls=['translate.googleapis.com'])


# results = model(source="C:/Users/96567/Desktop/Uni/Visual Impairment Aids project/Smart_Stick_Software/Repo/WIN_20240217_11_42_36_Pro.jpg", show=True, conf=0.25,save=True)
results = model("captured_image.jpg", conf=0.4, show=True)        #predicting

names = model.names     #list for accessing the class names of the prediction model

for r in results:       #looping over the results list
    for c in r.boxes.cls:       #getting each box in the result
        print(names[int(c)])        #getting the class name of the box i.e the object name
        ar = translator.translate(names[int(c)],dest='ar')
        print(ar)
        mp3_fp = BytesIO()
        tts = gTTS(ar, lang='ar')
        tts.save('hello.mp3')
        # tts.stream()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        sound = pygame.mixer.Sound(mp3_fp)
        playing = sound.play()
        while playing.get_busy():
             pygame.time.delay(100)
        time.sleep(0.5)
        mp3_fp.close()

