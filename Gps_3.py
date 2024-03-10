#pip install gps3

#//sudo apt update
#//sudo apt install python-gps





from gps3 import gps3

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
                    return latitude, longitude

    except KeyboardInterrupt:
        print("Exiting GPS reader")
    finally:
        gps_socket.close()

if __name__ == '__main__':
    latitude, longitude = read_gps_data()
    print("Latitude:", latitude)
    print("Longitude:", longitude)