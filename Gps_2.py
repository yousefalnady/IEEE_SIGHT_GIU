#sudo usermod -aG dialout aerobic





def read_gps_data():
    with open('/dev/ttyS0', 'r') as gps_serial:
        try:
            while True:
                line = gps_serial.readline().strip()
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

if __name__ == '__main__':
    print(read_gps_data())
    #latitude, longitude = read_gps_data()
    #print("Latitude:", latitude)
    #print("Longitude:", longitude)
