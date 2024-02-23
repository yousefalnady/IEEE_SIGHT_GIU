#libcamera-vid -n -t 0 --width 1280 --height 960 --framerate 1 --inline --listen -o tcp://127.0.0.1:8888
#the above line streams the camera feed to a certain tcp connection port which we will read from later on

from ultralytics import YOLO        #importing the ML library
from gtts import gTTS               #Google-Text-To-Speech API
from io import BytesIO              #File handling library to play audio
import pygame                       #for playing audio
import time
import picamera


model = YOLO('yolov8n.pt')          #selecting the prediction model
pygame.init()
pygame.mixer.init()

def Process(x):
    # results = model(source="C:/Users/96567/Desktop/Uni/Visual Impairment Aids project/Smart_Stick_Software/Repo/WIN_20240217_11_42_36_Pro.jpg", show=True, conf=0.25,save=True)
    # results = model("0", conf=0.25, show=True)        #predicting
    
    results = model('tcp://127.0.0.1:8888', stream=True)        #predicting
    names = model.names     #list for accessing the class names of the prediction model

    for r in results:       #looping over the results list
        for c in r.boxes.cls:       #getting each box in the result
            print(names[int(c)])        #getting the class name of the box i.e the object name
            mp3_fp = BytesIO()
            tts = gTTS(names[int(c)], lang='fr')
            tts.save('hello.mp3')
            # tts.stream()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            sound = pygame.mixer.Sound(mp3_fp)
            sound.play()
            time.sleep(0.5)
            mp3_fp.close()

if  __name__ == "__main__":
    Process()