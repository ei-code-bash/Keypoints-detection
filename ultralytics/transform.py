from ultralytics import YOLO
model= YOLO('yolov8n-pose.pt')
model=YOLO('best.pt')
model.export(format='onnx') 