from time import sleep
import picamera

def cam():
    camera = PiCamera()

    camera.start_preview()
    sleep(15)
    camera.stop_preview()

if  __name__ == "__main__":
    cam()