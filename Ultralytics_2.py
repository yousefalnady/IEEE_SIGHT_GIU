#pip install googletrans==4.0.0-rc1
from ultralytics import YOLO        #importing the ML library
from gtts import gTTS               #Google-Text-To-Speech API
from io import BytesIO              #File handling library to play audio
import pygame                       #for playing audio
import time
from googletrans import Translator


model = YOLO('yolov8n.pt')          #selecting the prediction model
pygame.init()
pygame.mixer.init()
translator = Translator()


# results = model(source="C:/Users/96567/Desktop/Uni/Visual Impairment Aids project/Smart_Stick_Software/Repo/WIN_20240217_11_42_36_Pro.jpg", show=True, conf=0.25,save=True)
results = model("C:/Users/96567/Desktop/Uni/Visual Impairment Aids project/Smart_Stick_Software/Repo/coffee.jpg", conf=0.25, show=True)        #predicting

names = model.names     #list for accessing the class names of the prediction model

for r in results:       #looping over the results list
    for c in r.boxes.cls:       #getting each box in the result
        print(names[int(c)])        #getting the class name of the box i.e the object name
        ar = translator.translate(names[int(c)],dest='ar')
        print(ar)
        mp3_fp = BytesIO()
        tts = gTTS(ar.text, lang='ar')
        tts.save('hello.mp3')
        # tts.stream()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        sound = pygame.mixer.Sound(mp3_fp)
        sound.play()
        time.sleep(0.5)
        mp3_fp.close()

