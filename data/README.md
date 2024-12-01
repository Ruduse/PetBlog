1. Cấu trúc thư mục Dataset
dataset/
├── images/
│   ├── train/
│   ├── val/
│   ├── test/ (tuỳ chọn)
├── labels/
│   ├── train/
│   ├── val/
│   ├── test/ (tuỳ chọn)
├── data.yaml

Bước 1: Chuẩn bị dữ liệu ảnh và nhãn
Dữ liệu cần có:(dữ liệu thô)

Hình ảnh (.jpg): Lưu trong thư mục images/.
Nhãn annotation (.txt): Lưu trong thư mục labels/.
Mỗi file .txt phải có cùng tên với file ảnh tương ứng. Ví dụ:
images/
├── image1.jpg
├── image2.jpg

labels/
├── image1.txt
├── image2.txt
2. Gán nhãn (Annotation) cho dữ liệu
Đảm bảo định dạng nhãn:
Mỗi file .txt chứa thông tin bounding box theo định dạng YOLO:

php
<class_id> <x_center> <y_center> <width> <height>
Ví dụ:

0 0.5 0.5 0.2 0.3
1 0.3 0.7 0.1 0.1
Nguồn dữ liệu:

Tải về từ các dataset công khai như COCO, Pascal VOC, hoặc Roboflow.
Tự gán nhãn bằng công cụ:
LabelImg: Hỗ trợ xuất nhãn định dạng YOLO.
Roboflow: Hỗ trợ annotation online.
Bước 2: Đặt dữ liệu vào thư mục ban đầu
Trước khi chạy đoạn code, tổ chức dữ liệu như sau:

Bước 3: Di chuyển file nhãn sang thư mục riêng (nếu cần)
Khi gán nhãn, các file .txt thường được lưu trong thư mục images/ cùng với hình ảnh. Bạn có thể chuyển chúng sang thư mục labels/ bằng một đoạn script Python đơn giản:

python
Copy code
import os
import shutil

image_dir = "images/"
label_dir = "labels/"

os.makedirs(label_dir, exist_ok=True)

# Di chuyển tất cả file .txt từ thư mục images sang labels
for file in os.listdir(image_dir):
    if file.endswith(".txt"):
        shutil.move(os.path.join(image_dir, file), os.path.join(label_dir, file))
Copy code
project/
├── images/
│   ├── image1.jpg
│   ├── image2.jpg
│   ├── ...
├── labels/
│   ├── image1.txt
│   ├── image2.txt
│   ├── ...

3. Tạo file cấu hình data.yaml
path: ./dataset          # Đường dẫn đến thư mục dataset
train: images/train      # Đường dẫn tập train
val: images/val          # Đường dẫn tập validation
test: images/test        # Đường dẫn tập test (tuỳ chọn)
nc: 2                    # Số lượng class
names: ["class1", "class2"]  # Danh sách tên các class

4. Chia tập dữ liệu (Train, Val, Test)
 --->Chạy đoạn code test.py
Tác dụng: Code này sẽ:

Tạo thư mục dataset/ để lưu trữ các tập con:
bash
Copy code
dataset/
├── images/
│   ├── train/
│   ├── val/
│   ├── test/
├── labels/
│   ├── train/
│   ├── val/
│   ├── test/
Tự động chia ảnh và nhãn tương ứng theo tỷ lệ: 80% train, 10% val, 10% test.
Copy các file ảnh và nhãn vào thư mục tương ứng.
Yêu cầu:

Thư viện Python: os, shutil, và scikit-learn.
Đảm bảo rằng tất cả ảnh đều có file nhãn đi kèm và ngược lại.
Bước 4: Kiểm tra kết quả
Sau khi chạy xong:

Kiểm tra thư mục dataset/ để đảm bảo tất cả ảnh và nhãn đã được chia đúng.
Nếu có lỗi:
Kiểm tra xem thư mục images/ và labels/ đã có đủ dữ liệu chưa.
Đảm bảo file nhãn .txt đúng định dạng.
5. Kiểm tra dữ liệu
Sử dụng thư viện như ultralytics để kiểm tra dữ liệu sau khi chuẩn bị:

python
Copy code
from ultralytics import YOLO

# Kiểm tra dataset
model = YOLO('yolov8n.pt')  # Load mô hình YOLOv8
model.train(data='data.yaml', epochs=1, imgsz=640)  # Chạy kiểm tra nhanh
6. Huấn luyện YOLOv8
Sau khi có dataset đầy đủ, bạn có thể dùng nó để train mô hình YOLO.
Sử dụng Ultralytics YOLOv8:

bash
Copy code
yolo train model=yolov8n.pt data=dataset/data.yaml epochs=50 imgsz=640


<!-- 
Giả sử bạn có 5 bức ảnh dùng cho bài toán phát hiện đối tượng, thư mục hình ảnh sẽ được tổ chức như sau:

Copy code
images/
├── cat1.jpg
├── cat2.jpg
├── dog1.jpg
├── dog2.jpg
├── bird1.jpg
Trong đó:

cat1.jpg, cat2.jpg: Ảnh về mèo.
dog1.jpg, dog2.jpg: Ảnh về chó.
bird1.jpg: Ảnh về chim.
Thêm file nhãn sau khi gán nhãn
Khi bạn sử dụng công cụ gán nhãn như LabelImg, mỗi ảnh sẽ có một file nhãn .txt tương ứng được tạo ra trong cùng thư mục hoặc thư mục khác, ví dụ:

Copy code
images/
├── cat1.jpg
├── cat1.txt
├── cat2.jpg
├── cat2.txt
├── dog1.jpg
├── dog1.txt
├── dog2.jpg
├── dog2.txt
├── bird1.jpg
├── bird1.txt
Nội dung file nhãn (cat1.txt):
plaintext
Copy code
0 0.5 0.5 0.3 0.4
1 0.7 0.8 0.2 0.1
Dòng 1: Đối tượng thuộc class 0 (mèo), với tọa độ và kích thước bounding box.
Dòng 2: Đối tượng thuộc class 1 (chó), với tọa độ và kích thước bounding box.
Tách file nhãn sang thư mục labels/
Sau khi gán nhãn, bạn có thể di chuyển file .txt sang một thư mục riêng labels/:

Copy code
images/
├── cat1.jpg
├── cat2.jpg
├── dog1.jpg
├── dog2.jpg
├── bird1.jpg

labels/
├── cat1.txt
├── cat2.txt
├── dog1.txt
├── dog2.txt
├── bird1.txt
 -->
 
chạy script chia dataset

import os
import shutil
from sklearn.model_selection import train_test_split

# Đường dẫn dữ liệu gốc
image_dir = "images/"
label_dir = "labels/"

# Tạo thư mục output
for split in ["train", "val", "test"]:
    os.makedirs(f"dataset/images/{split}", exist_ok=True)
    os.makedirs(f"dataset/labels/{split}", exist_ok=True)

# Lấy danh sách file ảnh
images = [f for f in os.listdir(image_dir) if f.endswith(".jpg")]
labels = [f.replace(".jpg", ".txt") for f in images]

# Chia tập dữ liệu
train_images, val_images = train_test_split(images, test_size=0.2, random_state=42)
val_images, test_images = train_test_split(val_images, test_size=0.5, random_state=42)

# Copy dữ liệu
def move_files(images, split):
    for image in images:
        shutil.copy(image_dir + image, f"dataset/images/{split}/{image}")
        shutil.copy(label_dir + image.replace(".jpg", ".txt"), f"dataset/labels/{split}/{image.replace('.jpg', '.txt')}")

move_files(train_images, "train")
move_files(val_images, "val")
move_files(test_images, "test")
