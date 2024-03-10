import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO_ECHO1 = 13
GPIO_TRIG1 = 11
GPIO_ECHO2 = 2
GPIO_TRIG2 = 3
GPIO_ECHO3 = 17
GPIO_TRIG3 = 27
Vibration_Motor1 = 18
Vibration_Motor2 = 20
Vibration_Motor3 = 21

GPIO.setup(GPIO_TRIG1, GPIO.OUT)
GPIO.setup(GPIO_ECHO1, GPIO.IN)
GPIO.setup(GPIO_TRIG2, GPIO.OUT)
GPIO.setup(GPIO_ECHO2, GPIO.IN)
GPIO.setup(GPIO_TRIG3, GPIO.OUT)
GPIO.setup(GPIO_ECHO3, GPIO.IN)
GPIO.setup(Vibration_Motor1, GPIO.OUT)
GPIO.setup(Vibration_Motor2, GPIO.OUT)
GPIO.setup(Vibration_Motor3, GPIO.OUT)

GPIO.output(GPIO_TRIG1, False)
GPIO.output(GPIO_TRIG2, False)
GPIO.output(GPIO_TRIG3, False)
GPIO.output(Vibration_Motor1, False)
GPIO.output(Vibration_Motor2, False)
GPIO.output(Vibration_Motor3, False)

time.sleep(2)

def ultrasonic(GPIO_TRIG, GPIO_ECHO):
    GPIO.output(GPIO_TRIG, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIG, False)
    
    pulse_start = time.time()
    pulse_end = time.time()
    
    while GPIO.input(GPIO_ECHO) == 0:
        pulse_start = time.time()
        
    while GPIO.input(GPIO_ECHO) == 1:
        pulse_end = time.time()
        
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

try:
    while True:
        distance1 = ultrasonic(GPIO_TRIG1, GPIO_ECHO1)
        distance2 = ultrasonic(GPIO_TRIG2, GPIO_ECHO2)
        distance3 = ultrasonic(GPIO_TRIG3, GPIO_ECHO3)
        
        print("Distance 1:", distance1, "cm")
        print("Distance 2:", distance2, "cm")
        print("Distance 3:", distance3, "cm")
        
        min_distance = min(distance1, distance2, distance3)
        if min_distance == distance1:
            min_sensor = "Ultrasonic 1"
        elif min_distance == distance2:
            min_sensor = "Ultrasonic 2"
        else:
            min_sensor = "Ultrasonic 3"
        print("Minimum Distance:",min_distance)
        print(min_sensor)
        if min_distance < 10 and min_sensor=="Ultrasonic 1":
            GPIO.output(Vibration_Motor1, True)
            print("Minimum Distance2:",min_distance)
            time.sleep(4)
            GPIO.output(Vibration_Motor1, False)
        elif min_distance < 10 and min_sensor=="Ultrasonic 2":
            GPIO.output(Vibration_Motor2, True)
            print("Minimum Distance2:",min_distance)
            time.sleep(4)
       
            GPIO.output(Vibration_Motor2, False)
        elif min_distance < 10 and min_sensor=="Ultrasonic 3":
            GPIO.output(Vibration_Motor3, True)
            print("Minimum Distance2:",min_distance)
            time.sleep(4)	
        
            GPIO.output(Vibration_Motor3, False)            
        time.sleep(0.1)
        
except KeyboardInterrupt:
    GPIO.cleanup()