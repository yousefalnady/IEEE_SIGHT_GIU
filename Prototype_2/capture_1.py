import cv2

def capture_image():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    ret, frame = cap.read()

    if ret:
        cv2.imwrite('captured_image.jpg', frame)
        print("Image captured successfully.")
    else:
        print("Error: Could not capture image.")

    cap.release()


capture_image()
