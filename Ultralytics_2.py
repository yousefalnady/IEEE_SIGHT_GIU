from ultralytics import YOLO        #importing the ML library

model = YOLO('yolov8n.pt')          #selecting the prediction model

# results = model(source="C:/Users/96567/Desktop/Uni/Visual Impairment Aids project/Smart_Stick_Software/Repo/WIN_20240217_11_42_36_Pro.jpg", show=True, conf=0.25,save=True)
results = model("people.jpg", save_txt=True)        #predicting
# results = model(source="0", show=True, conf=0.4,stream=True)

names = model.names     #list for accessing the class names of the prediction model

for r in results:       #looping over the results list
    for c in r.boxes.cls:       #getting each box in the result
        print(names[int(c)])        #getting the class name of the box i.e the object name


# for x in results:
#     print(x.tojson())

# print(results[0].tojson())
