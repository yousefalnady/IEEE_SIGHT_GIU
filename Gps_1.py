#sudo apt update
#sudo apt install python-serial





import serial

def read_gps_data():
    ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)  # Adjust port and baud rate as needed

    try:
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line.startswith('$GPGGA'):
                data = line.split(',')
                if len(data) >= 10 and data[6] != '' and data[7] != '':
                    latitude = float(data[2][:2]) + float(data[2][2:]) / 60
                    if data[3] == 'S':
                        latitude = -latitude
                    longitude = float(data[4][:3]) + float(data[4][3:]) / 60
                    if data[5] == 'W':
                        longitude = -longitude
                    return latitude, longitude
    except KeyboardInterrupt:
        print("Exiting GPS reader")
    finally:
        ser.close()

if __name__ == '__main__':
    print(read_gps_data())
    #latitude, longitude = read_gps_data()
    #print("Latitude:", latitude)
    #print("Longitude:", longitude)
