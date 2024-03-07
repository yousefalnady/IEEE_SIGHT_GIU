import cv2

def capture_image():
    # Open a connection to the webcam (camera index 0 by default)
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened successfully
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Capture a single frame
    ret, frame = cap.read()

    # Save the captured frame to an image file
    if ret:
        cv2.imwrite('captured_image.jpg', frame)
        print("Image captured successfully.")
    else:
        print("Error: Could not capture image.")

    # Release the webcam
    cap.release()

# Call the function to capture an image
capture_image()