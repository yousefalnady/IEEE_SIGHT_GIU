import requests
import time
from gtts import gTTS  # Import the Google Text-to-Speech library
import tempfile  # Import the tempfile module for creating temporary files
import pygame  # Import pygame for playing audio
import re  # Import the regular expression module

# Initialize pygame audio mixer
pygame.mixer.init()

# Rehab 
rehab_egypt = (29.9792, 31.1342)

# North 90 Street
current_location = (30.0363, 31.4758)

def contains_arabic(text):
    """
    Function to check the presence of Arabic words in the instructions.
    """
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+')
    return bool(arabic_pattern.search(text))

def speak(text, lang='en'):
    """
    Function to speak the given text using Google Text-to-Speech.
    """
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False) as fp:
        tts.save(f"{fp.name}.mp3")
        pygame.mixer.music.load(f"{fp.name}.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

def navigate_to(destination):
    """
    Function to navigate to a destination.
    """
    # Construct the URL for OpenRouteService Directions API
    url = f"https://api.openrouteservice.org/v2/directions/foot-walking?api_key=5b3ce3597851110001cf624802cda44b3896483284d823f2826650e8&start={current_location[1]},{current_location[0]}&end={destination[1]},{destination[0]}"
    # Send a request to the OpenRouteService Directions API
    response = requests.get(url)
    # Check the response status
    if response.status_code != 200:
        print(f"Error: Unable to retrieve navigation data. Status code: {response.status_code}")
        return
    
    # Parse the response as JSON
    data = response.json()

    # Check if the response contains route information
    if 'features' in data:
        # Extract steps from the response
        steps = data['features'][0]['properties']['segments'][0]['steps']
        
        if steps:
            print(f"Navigation to {destination}:")
            for step in steps:
                instruction = step.get('instruction', '')
                if instruction:
                    step_id = step.get('id', '')
                    print(f"Step {step_id}: {instruction}")
                    
                    # Split instruction into English and Arabic parts
                    english_parts = []
                    arabic_parts = []
                    for part in instruction.split():
                        if contains_arabic(part):
                            arabic_parts.append(part)
                        else:
                            english_parts.append(part)
                    # Speak English parts
                    if english_parts:
                        speak(' '.join(english_parts))
                    # Speak Arabic parts
                    if arabic_parts:
                        speak(' '.join(arabic_parts), lang='ar')
                    time.sleep(3)  # Wait for 3 seconds between instructions
                else:
                    print("No detailed instruction available for this step.")
        else:
            print("No route found.")
    else:
        print("No route found.")

# Navigate to the destination
navigate_to(rehab_egypt)

print("Navigation complete!")
