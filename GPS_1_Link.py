#sudo apt update
#sudo apt install python-serial





import serial
from pushbullet import pushbullet as pbclient

pb = pbclient.Pushbullet("o.OvzdycciHIRvvwJKmEJXEwj5Si3gTEuJ")

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
                    map_link = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
                    return latitude, longitude, map_link
    except KeyboardInterrupt:
        print("Exiting GPS reader")
    finally:
        ser.close()

if __name__ == '__main__':
    x = read_gps_data()
    print(x)
    mydev = pb.get_device('Samsung SM-A736B')
	#pushing a notification to my phone
    push = mydev.push_note("message",str(read_gps_data()))
    print('notification sent to user')
    #latitude, longitude = read_gps_data()
    #print("Latitude:", latitude)
    #print("Longitude:", longitude)
