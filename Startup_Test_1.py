import pygame
from io import BytesIO
from gtts import gTTS
import time

pygame.init()
pygame.mixer.init()


for i in range(3):
    mp3_fp = BytesIO()
    tts = gTTS('This is a startup test using just audio as the easiest method to test', lang='en')
    tts.save('statrup_audio.mp3')
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
            
    # Play the translated audio
    sound = pygame.mixer.Sound(mp3_fp)
    playing = sound.play()
    while playing.get_busy():
        pygame.time.delay(100)
    time.sleep(0.5)
    mp3_fp.close()
