pip install gps3

//sudo apt update
//sudo apt install python-gps




from gps3 import gps3
from pushbullet import Pushbullet

# Pushbullet API key
PUSHBULLET_API_KEY = "YOUR_PUSHBULLET_API_KEY"

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
                    map_link = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
                    return latitude, longitude, map_link

    except KeyboardInterrupt:
        print("Exiting GPS reader")
    finally:
        gps_socket.close()

def send_notification(title, body):
    pb = Pushbullet(PUSHBULLET_API_KEY)
    pb.push_link(title, body)

if __name__ == '__main__':
    latitude, longitude, map_link = read_gps_data()
    print("Latitude:", latitude)
    print("Longitude:", longitude)
    print("Map Link:", map_link)
    
    if map_link:
        # Send the map link as a notification using Pushbullet
        send_notification("Location Update", map_link)

