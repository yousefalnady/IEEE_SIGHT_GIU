import requests
import time
from gtts import gTTS
import tempfile
import pygame
import re
import serial
import gpsd

# Initialize pygame audio mixer
pygame.mixer.init()

# Rehab Egypt
rehab_egypt = (29.9792, 31.1342)
current_location = None

def contains_arabic(text):
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+')
    return bool(arabic_pattern.search(text))

def speak(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False) as fp:
        tts.save(f"{fp.name}.mp3")
        pygame.mixer.music.load(f"{fp.name}.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

def read_gps_data():
    gpsd.connect()
    packet = gpsd.get_current()
    return packet.position()

def navigate_to(destination):
    while True:
        latitude, longitude = read_gps_data()
        current_location = (latitude, longitude)

        # Check if destination is reached
        if current_location and distance(current_location, destination) <= 2:
            print("Destination reached!")
            break
        url = f"https://api.openrouteservice.org/v2/directions/foot-walking?api_key=5b3ce3597851110001cf624802cda44b3896483284d823f2826650e8&start={current_location[1]},{current_location[0]}&end={destination[1]},{destination[0]}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error: Unable to retrieve navigation data. Status code: {response.status_code}")
            return        
        data = response.json()
        if 'features' in data:
            steps = data['features'][0]['properties']['segments'][0]['steps']            
            if steps:
                print(f"Navigation to {destination}:")
                for step in steps:
                    instruction = step.get('instruction', '')
                    if instruction:
                        step_id = step.get('id', '')
                        print(f"Step {step_id}: {instruction}")                        
                        english_parts = []
                        arabic_parts = []
                        for part in instruction.split():
                            if contains_arabic(part):
                                arabic_parts.append(part)
                            else:
                                english_parts.append(part)
                        if english_parts:
                            speak(' '.join(english_parts))
                        if arabic_parts:
                            speak(' '.join(arabic_parts), lang='ar')
                        time.sleep(3)  # Wait for 3 seconds between instructions
                    else:
                        print("No detailed instruction available for this step.")
            else:
                print("No route found.")
        else:
            print("No route found.")

def distance(coord1, coord2):
    return geodesic(coord1, coord2).meters

navigate_to(rehab_egypt)

print("Navigation complete!")
