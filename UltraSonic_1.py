import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO_ECHO1 = 13
GPIO_TRIG1= 11
GPIO_ECHO2 = 2
GPIO_TRIG2 = 3
GPIO_ECHO3 = 17
GPIO_TRIG3 = 27
Vibration_Motor = 18
GPIO.setup(GPIO_ECHO1,GPIO.IN)
GPIO.setup(GPIO_TRIG1,GPIO.OUT)
GPIO.setup(GPIO_ECHO2,GPIO.IN)
GPIO.setup(GPIO_TRIG2,GPIO.OUT)
GPIO.setup(GPIO_ECHO3,GPIO.IN)
GPIO.setup(GPIO_TRIG3,GPIO.OUT)
GPIO.setup(Vibration_Motor,GPIO.OUT)
GPIO.output(GPIO_TRIG1, GPIO.LOW)
GPIO.output(GPIO_TRIG2, GPIO.LOW)
GPIO.output(GPIO_TRIG3, GPIO.LOW)
GPIO.output(Vibration_Motor, GPIO.LOW)
time.sleep(2)
def ultrasonic():
    GPIO.output(GPIO_TRIG1, GPIO.HIGH)
    GPIO.output(GPIO_TRIG2, GPIO.HIGH)
    GPIO.output(GPIO_TRIG3, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIG1, GPIO.LOW)
    GPIO.output(GPIO_TRIG2, GPIO.LOW)
    GPIO.output(GPIO_TRIG3, GPIO.LOW)
    
	while GPIO.input(GPIO_ECHO1)==0:
		start_time1 = time.time()        
    while GPIO.input(GPIO_ECHO1)==1:
		Bounce_back_time1 = time.time()               
    while GPIO.input(GPIO_ECHO2)==0:
		start_time2 = time.time()
    while GPIO.input(GPIO_ECHO2)==1:
		Bounce_back_time2 = time.time()
    while GPIO.input(GPIO_ECHO3)==0:
		start_time3 = time.time()
    while GPIO.input(GPIO_ECHO3)==1:
		Bounce_back_time3 = time.time()
    pulse_duration1 = Bounce_back_time1 - start_time1
    pulse_duration2 = Bounce_back_time2 - start_time2
    pulse_duration3 = Bounce_back_time3 - start_time3
    distance1 = round(pulse_duration1 * 17150, 2)
    distance2 = round(pulse_duration2 * 17150, 2)
    distance3 = round(pulse_duration3 * 17150, 2)
    print ("Distance 1:", distance1)
    print ("Distance 2:",distance2)
    print ("Distance 3:", distance3)
    distance = min(distance1, distance2, distance3)
    print ("Minimum Distance:", distance)
    return(distance)

try:
    while True:
        distance = ultrasonic()
        if distance<10:
            GPIO.output(Vibration_Motor, GPIO.HIGH)
        else:
            GPIO.output(Vibration_Motor, GPIO.LOW)
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
