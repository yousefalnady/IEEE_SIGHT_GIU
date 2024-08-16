import serial
import time

def parse_gpgga(sentence):
    # Sample parsing logic, replace with your preferred method
    data = sentence.split(',')
    if len(data) >= 6:
        latitude = float(data[2])
        longitude = float(data[4])
        # ... extract other data as needed
        return latitude, longitude
    else:
        return None, None

ser = serial.Serial('/dev/ttyTHS1', 9600)  # Replace with correct port

while True:
    line = ser.readline().decode('utf-8').rstrip()
    if line.startswith('$GPGGA'):
        latitude, longitude = parse_gpgga(line)
        if latitude and longitude:
            print(f"Latitude: {latitude}, Longitude: {longitude}")
            # Do something with the GPS data
    time.sleep(1)  # Adjust sleep time as needed

