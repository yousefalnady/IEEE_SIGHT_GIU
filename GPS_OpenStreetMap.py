#pip install pushbullet.py

import webbrowser
import requests
from gps3 import gps3
from pushbullet import Pushbullet

PUSHBULLET_API_KEY = "KEYYYYYYY"

def reverse_geocode(latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        address = data.get('display_name')
        return address
    return None

def read_gps_data():
    gps_socket = gps3.GPSDSocket()
    data_stream = gps3.DataStream()

    try:
        gps_socket.connect()
        gps_socket.watch()

        for new_data in gps_socket:
            if new_data:
                data_stream.unpack(new_data)
                if data_stream.TPV['lat'] != 'n/a' and data_stream.TPV['lon'] != 'n/a':
                    latitude = data_stream.TPV['lat']
                    longitude = data_stream.TPV['lon']
                    location_data = reverse_geocode(latitude, longitude)
                    if location_data:
                        return latitude, longitude, location_data
                    else:
                        return latitude, longitude

    except KeyboardInterrupt:
        print("Exiting GPS reader")
    finally:
        gps_socket.close()

def send_notification(title, body):
    pb = Pushbullet(KEYYYYYYY)
    pb.push_note(title, body)

if __name__ == '__main__':
    latitude, longitude, address = read_gps_data()
    print("Latitude:", latitude)
    print("Longitude:", longitude)
    print("Address:", address)
    
    if address:
        send_notification("Location Update", address)




#Latitude: 30.0443879
#Longitude: 31.2357257
#Address: سوق الجملة، منطقة عين شمس الشرقية، قسم عين شمس، محافظة القاهرة‬، مصر
