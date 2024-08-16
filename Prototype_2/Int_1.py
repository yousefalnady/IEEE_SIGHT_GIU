import jetson.inference
import jetson.utils
import time
import cv2
import RPi.GPIO as GPIO

# Set up GPIO
BUTTON_PIN = 18  # Change this to the GPIO pin you are using for the button
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set button pin as input with pull-up resistor

def capture_image():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return None

    ret, frame = cap.read()

    if ret:
        print("Image captured successfully.")
        # Convert frame to CUDA memory and perform detection on it
        img = jetson.utils.cudaFromNumpy(frame)
        detections = net.Detect(img)
        # Print detection results
        print("Detected {} objects:".format(len(detections)))
        for detection in detections:
            class_id = detection.ClassID
            class_name = net.GetClassDesc(class_id)  # Get class name using the class ID
            print(" - Class Name: {}, Confidence: {:.2f}, Bounding Box: [{}, {}, {}, {}]"
                  .format(class_name, detection.Confidence, detection.Left, detection.Top, detection.Right, detection.Bottom))

        # Convert image back to NumPy format and save the original file
        cv2.imwrite('captured_image.jpg', cv2.cvtColor(jetson.utils.cudaToNumpy(img), cv2.COLOR_BGR2RGB))

        return img
    else:
        print("Error: Could not capture image.")
        return None

    cap.release()

# Load the DetectNet model
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)

print("Press the button to capture an image and detect objects. Press Ctrl+C to exit.")

try:
    while True:
        # Wait for the button press
        GPIO.wait_for_edge(BUTTON_PIN, GPIO.FALLING)  # Wait for button press (falling edge)
        
        # Capture an image and perform detection
        img = capture_image()

        # Check if image capture was successful
        if img is None:
            # Handle error (e.g., continue or exit)
            print("Failed to capture image. Skipping detection.")
            continue

        # Debounce delay to prevent multiple captures from a single press
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Exiting program.")

finally:
    GPIO.cleanup()  # Clean up GPIO settings
