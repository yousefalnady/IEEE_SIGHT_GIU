import multiprocessing as mp
import numpy as np
import osmnx as ox
from googletrans import Translator
import matplotlib.pyplot as plt
import time
import pygame
from io import BytesIO
from gtts import gTTS

pygame.init()
pygame.mixer.init()

translator = Translator(service_urls=['translate.googleapis.com'])


def resolve_route(route, graph):
    directions = []
    for i in range(len(route) - 1):
        current_node = route[i]
        next_node = route[i + 1]
        edge = graph[current_node][next_node][0]  # Get the edge between current and next nodes
        street_name = edge.get('name', 'Unnamed')
        directions.append(f"Go on {street_name}")
    return directions


np.random.seed(0)
ox.__version__
place = "5th settlement, New Cairo, Cairo, Egypt"
#place = "Piedmont, California, USA"
G = ox.graph_from_place(place, network_type="walk")
G = ox.speed.add_edge_speeds(G)
G = ox.speed.add_edge_travel_times(G)

orig = ox.distance.nearest_nodes(G, X=31.426599, Y=29.99937)
dest = ox.distance.nearest_nodes(G, X=31.421820, Y=30.002794)
route = ox.shortest_path(G, orig, dest, weight="travel_time")
print(route)


Gp = ox.project_graph(G)
#ox.plot_graph(G)
ox.plot_graph_route(G,route)

directions = resolve_route(route,G)

for i, direction in enumerate(directions):
    print(f"{i+1}. {direction}")
    mp3_fp = BytesIO()
    tts = gTTS(direction, lang='ar')
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

# for i, direction in enumerate(directions):
#     time.sleep(8)
#     translation = translator.translate(directions, dest='ar')
#     translated_text = translation.text
#     print(translated_text)

