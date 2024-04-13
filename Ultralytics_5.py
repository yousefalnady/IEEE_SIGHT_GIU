import cv2
from ultralytics import YOLO
from gtts import gTTS
from io import BytesIO
import pygame
from googletrans import Translator
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


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


print('Waiting for button press...')
while True:
    if GPIO.input(22) == GPIO.HIGH:
        print("Button was pushed!")
        break
print('Button pressed.')

capture_image()

model = YOLO('yolov8n.pt')
pygame.init()
pygame.mixer.init()
translator = Translator(service_urls=['translate.googleapis.com'])

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
