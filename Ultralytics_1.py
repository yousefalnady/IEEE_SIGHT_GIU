from ultralytics import YOLO
model = YOLO('yolov8s.pt')
results = model(source="C:/Users/96567/Desktop/3-1920x1080-2d0741389a27fd438c44e5ff90d27b39.jpg", show=True, conf=0.4, save=True)