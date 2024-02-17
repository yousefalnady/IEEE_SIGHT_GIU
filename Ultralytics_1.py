import numpy
from ultralytics import YOLO
model = YOLO('yolov8s.pt')
results = model(source="C:/Users/96567/Desktop/Uni/Visual Impairment Aids project/Smart_Stick_Software/Repo/WIN_20240217_11_42_36_Pro.jpg", show=True, conf=0.4, save=True)