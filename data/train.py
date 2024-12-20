from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.yaml")  # build a new model from scratch

# Use the model
results = model.train(data="C:/Users/rimdang/Project/PetBlog/data.yaml", epochs=100)
