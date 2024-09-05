import serial
import time

# Initialize the serial connection
ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)

def get_location():
    # Send AT command to check if the GPS is ready
    ser.write(b'AT+CGPSSTATUS?\r\n')
    response = ser.readline().decode().strip()
    print(response)
    if 'LOCATION' in response:
        # Send AT command to get the GPS data
        ser.write(b'AT+CGPSINF=0\r\n')
        gps_data = ser.readline().decode().strip()
        # Parse the GPS data
        latitude, longitude = parse_gps_data(gps_data)
        return latitude, longitude
    else:
        return None, None

def parse_gps_data(gps_data):
    # Implement your own logic to parse the GPS data
    # The format of the GPS data depends on the AT command used
    # Example: +CGPSINF: 1,<lat>,<long>,...
    parts = gps_data.split(',')
    latitude = float(parts[1])
    longitude = float(parts[2])
    return latitude, longitude

while True:
    latitude, longitude = get_location()
    if latitude is not None and longitude is not None:
        print(f"Latitude: {latitude}, Longitude: {longitude}")
    else:
        print("GPS data not available")
    time.sleep(5)
