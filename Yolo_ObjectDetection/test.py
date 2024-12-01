# import os
# import cv2
# import numpy as np
# import random
# import shutil
# from ultralytics import YOLO
# from sklearn.model_selection import train_test_split

# # Tạo thư mục dữ liệu
# dataset_path = "dataset"
# os.makedirs(dataset_path, exist_ok=True)
# os.makedirs(f"{dataset_path}/images", exist_ok=True)
# os.makedirs(f"{dataset_path}/labels", exist_ok=True)

# # Tạo ảnh giả lập (thay bằng ảnh thực nếu có)
# for i in range(10):  # Tạo 10 ảnh giả lập
#     img = (np.random.rand(480, 640, 3) * 255).astype(np.uint8)  # Ảnh nhiễu ngẫu nhiên
#     label = f"0 {random.uniform(0, 1):.2f} {random.uniform(0, 1):.2f} 0.1 0.1"  # Nhãn ngẫu nhiên
#     cv2.imwrite(f"{dataset_path}/images/{i}.jpg", img)
#     with open(f"{dataset_path}/labels/{i}.txt", "w") as f:
#         f.write(label)

# # Chia tập train/test
# images = os.listdir(f"{dataset_path}/images")
# train_images, test_images = train_test_split(images, test_size=0.2, random_state=42)

# # Tạo thư mục train/test
# os.makedirs(f"{dataset_path}/images/train", exist_ok=True)
# os.makedirs(f"{dataset_path}/images/test", exist_ok=True)
# for img in test_images:
#     shutil.move(f"{dataset_path}/images/{img}", f"{dataset_path}/images/test/{img}")
# for img in train_images:
#     shutil.move(f"{dataset_path}/images/{img}", f"{dataset_path}/images/train/{img}")

# # Tạo file data.yaml
# with open(f"{dataset_path}/data.yaml", "w") as f:
#     f.write(f"""
# train: {dataset_path}/images/train
# val: {dataset_path}/images/test
# nc: 1
# names: ['object']
# """)

# # Huấn luyện mô hình YOLO
# model = YOLO("yolov8n.pt")  # Khởi tạo YOLO
# model.train(
#     data=f"{dataset_path}/data.yaml",  # Đường dẫn đến file YAML
#     epochs=50,                        # Số epoch
#     imgsz=640,                        # Kích thước ảnh
#     batch=16,                         # Batch size
#     name="custom_yolo_model"          # Tên mô hình
# )

# # Kiểm tra mô hình
# results = model.val()
# print(results)  # Kết quả đánh giá như mAP, Precision, Recall

# # Dự đoán ảnh mới
# model = YOLO("runs/train/custom_yolo_model/weights/best.pt")  # Load trọng số
# img = cv2.imread("test_image.jpg")  # Thay bằng ảnh thực
# results = model(img, stream=True)

# # Hiển thị kết quả
# for r in results:
#     boxes = r.boxes
#     for box in boxes:
#         x1, y1, x2, y2 = map(int, box.xyxy[0])  # Toạ độ bounding box
#         conf = box.conf[0]                      # Độ tin cậy
#         cls = int(box.cls[0])                   # Lớp đối tượng
#         cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
#         cv2.putText(img, f"Object {conf:.2f}", (x1, y1-10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# cv2.imshow("Prediction", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# # Xuất mô hình
# model.export(format="onnx")  # Xuất mô hình
import os
import cv2
import numpy as np
import random
import shutil
from ultralytics import YOLO
from sklearn.model_selection import train_test_split

# Đường dẫn thư mục dữ liệu
dataset_path = "dataset"
images_path = f"{dataset_path}/images"
labels_path = f"{dataset_path}/labels"
train_path = f"{images_path}/train"
test_path = f"{images_path}/test"

# Tạo thư mục dữ liệu (nếu chưa tồn tại)
os.makedirs(images_path, exist_ok=True)
os.makedirs(labels_path, exist_ok=True)
os.makedirs(train_path, exist_ok=True)
os.makedirs(test_path, exist_ok=True)

# Tạo ảnh và nhãn giả lập nếu chưa tồn tại
if len(os.listdir(images_path)) == 0 or len(os.listdir(labels_path)) == 0:
    for i in range(10):  # Tạo 10 ảnh giả lập
        img = (np.random.rand(480, 640, 3) * 255).astype(np.uint8)  # Ảnh nhiễu ngẫu nhiên
        label = f"0 {random.uniform(0, 1):.2f} {random.uniform(0, 1):.2f} 0.1 0.1"  # Nhãn ngẫu nhiên
        cv2.imwrite(f"{images_path}/{i}.jpg", img)
        with open(f"{labels_path}/{i}.txt", "w") as f:
            f.write(label)

# Chia tập train/test (nếu thư mục train/test rỗng)
if len(os.listdir(train_path)) == 0 or len(os.listdir(test_path)) == 0:
    images = [img for img in os.listdir(images_path) if img.endswith(".jpg")]
    train_images, test_images = train_test_split(images, test_size=0.2, random_state=42)

    for img in test_images:
        shutil.move(f"{images_path}/{img}", f"{test_path}/{img}")
    for img in train_images:
        shutil.move(f"{images_path}/{img}", f"{train_path}/{img}")

# Tạo file data.yaml (nếu chưa tồn tại)
yaml_content = f"""
train: {train_path.replace("\\", "/")}
val: {test_path.replace("\\", "/")}
nc: 1
names: ['object']
"""
# Sử dụng raw string (r""), tránh vấn đề thoát ký tự
with open(f"{dataset_path}/data.yaml", "w") as f:
    f.write(f"""
train: {dataset_path.replace("\\", "/")}/images/train
val: {dataset_path.replace("\\", "/")}/images/test
nc: 1
names: ['object']
""")



# Huấn luyện mô hình YOLO
model = YOLO("yolov8n.pt")  # Khởi tạo YOLO
model.train(
    data=yaml_path,  # Đường dẫn đến file YAML
    epochs=50,       # Số epoch
    imgsz=640,       # Kích thước ảnh
    batch=16,        # Batch size
    name="custom_yolo_model"  # Tên mô hình
)

# Kiểm tra mô hình
results = model.val()
print(results)  # Kết quả đánh giá như mAP, Precision, Recall

# Dự đoán ảnh mới
test_image_path = "test_image.jpg"  # Thay bằng đường dẫn ảnh thực tế
if os.path.exists(test_image_path):
    img = cv2.imread(test_image_path)
    results = model(img, stream=True)

    # Hiển thị kết quả
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, f"Object {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("Prediction", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print(f"Test image '{test_image_path}' not found.")

# Xuất mô hình
model.export(format="onnx", dynamic=True, simplify=True, device="cpu")  # Xuất mô hình
