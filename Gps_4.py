#sudo apt-get install gpsd gpsd-clients python-gps
#sudo systemctl stop gpsd.socket
#sudo systemctl disable gpsd.socket
#sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock




import gps

def get_gps_data():
    # session = gps.gps("localhost", "2947")
    session = gps.gps("localhost", "3000")
    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

    try:
        while True:
            report = session.next()
            if report['class'] == 'TPV':
                if hasattr(report, 'lat') and hasattr(report, 'lon'):
                    latitude = getattr(report, 'lat', "0")
                    longitude = getattr(report, 'lon', "0")
                    return latitude, longitude
    except KeyboardInterrupt:
        print("Exiting GPS reader")
    finally:
        session.close()

if __name__ == '__main__':
    latitude, longitude = get_gps_data()
    print("Latitude:", latitude)
    print("Longitude:", longitude)
