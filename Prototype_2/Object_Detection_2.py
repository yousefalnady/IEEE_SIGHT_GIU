import jetson.inference
import jetson.utils
import time
import cv2

# Load the DetectNet model
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)


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

        cap.release()
        return img
    else:
        print("Error: Could not capture image.")
        cap.release()
        return None

    cap.release()

def Detect_Objects():
    img = capture_image()
    if img is None:
        # Handle error (e.g., continue or exit)
        print("Failed to capture image. Skipping detection.")
    else:
        
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